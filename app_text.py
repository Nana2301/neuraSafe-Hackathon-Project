import json
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify

app = Flask(__name__)

model = tf.keras.models.load_model(r"E:\dataset_neurasafe\neurasafe_text_model.keras")

with open(r"E:\dataset_neurasafe\label_map.json", "r") as f:
    label_map = json.load(f)

classes = label_map["classes"]


def contains_any(text, keywords):
    return any(keyword in text for keyword in keywords)


def generate_explanation(message, final_label, rule_reasons):
    lower_text = message.lower()

    detailed_reasons = []

    if contains_any(lower_text, ["urgent", "immediately", "act now", "final warning"]):
        detailed_reasons.append("This message creates urgency to pressure the user.")

    if contains_any(lower_text, ["otp", "password", "pin", "verification code"]):
        detailed_reasons.append("It asks for sensitive information such as OTP, PIN, or password.")

    if contains_any(lower_text, ["http", "www", ".com", "bit.ly"]):
        detailed_reasons.append("It contains a suspicious link.")

    if contains_any(lower_text, ["prize", "winner", "reward", "claim"]):
        detailed_reasons.append("It uses reward bait to attract clicks.")

    if contains_any(lower_text, ["bank", "verify", "account", "security alert"]):
        detailed_reasons.append("It may be pretending to be an official service or bank.")

    if contains_any(lower_text, ["loan", "instant loan", "approval", "cash", "money", "rm"]):
        detailed_reasons.append("It uses financial or loan bait to attract the victim.")

    if contains_any(lower_text, ["ic", "bank details", "bank info", "account number", "personal details"]):
        detailed_reasons.append("It requests personal or banking details that could be abused.")

    if contains_any(lower_text, ["no documents needed", "guaranteed approval", "easy approval"]):
        detailed_reasons.append("It makes unrealistic approval promises to gain trust quickly.")

    if detailed_reasons:
        return " ".join(detailed_reasons)

    if rule_reasons:
        return "This message triggered several suspicious patterns based on the hybrid AI and rule-based detection system."

    if final_label == "scam":
        return "The trained AI model detected strong scam-like wording patterns in this message."
    elif final_label == "suspicious":
        return "The trained AI model found suspicious patterns that should be checked carefully."
    else:
        return "The trained AI model found this message more consistent with normal safe communication."


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "NeuraSafe Text AI API is running"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Message is required"}), 400

        x = tf.constant([message], dtype=tf.string)
        probs = model(x, training=False).numpy()[0]

        pred_index = int(np.argmax(probs))
        predicted_label = classes[pred_index]
        confidence = round(float(np.max(probs)) * 100, 2)

        lower_text = message.lower()

        rule_reasons = []
        rule_score = 0

        # Urgency
        if contains_any(lower_text, ["urgent", "immediately", "act now", "final warning"]):
            rule_reasons.append("Uses urgency wording")
            rule_score += 20

        # Sensitive information
        if contains_any(lower_text, ["otp", "password", "pin", "verification code"]):
            rule_reasons.append("Requests sensitive information")
            rule_score += 30

        # Suspicious links
        if contains_any(lower_text, ["http", "www", ".com", "bit.ly"]):
            rule_reasons.append("Contains suspicious link")
            rule_score += 25

        # Bank / official impersonation
        if contains_any(lower_text, ["bank", "verify", "account", "security alert"]):
            rule_reasons.append("Pretends to be official service or bank")
            rule_score += 20

        # Reward / winner bait
        if contains_any(lower_text, ["winner", "prize", "reward", "claim"]):
            rule_reasons.append("Uses reward bait")
            rule_score += 15

        # Loan / money bait
        if contains_any(lower_text, ["loan", "instant loan", "approval", "rm", "cash", "money"]):
            rule_reasons.append("Uses financial or loan bait")
            rule_score += 20

        # Personal / bank details
        if contains_any(lower_text, ["ic", "bank details", "bank info", "account number", "personal details"]):
            rule_reasons.append("Requests personal or banking details")
            rule_score += 25

        # Unrealistic promise
        if contains_any(lower_text, ["no documents needed", "guaranteed approval", "easy approval"]):
            rule_reasons.append("Uses unrealistic approval promise")
            rule_score += 20

        # Final hybrid decision
        if rule_score >= 45:
            final_label = "scam"
        elif rule_score >= 20:
            final_label = "suspicious"
        else:
            final_label = predicted_label

        # Strong override for known-dangerous combinations
        if predicted_label == "safe":
            if contains_any(lower_text, ["otp"]) and contains_any(lower_text, ["http", "www", ".com", "bit.ly"]):
                final_label = "scam"
            elif contains_any(lower_text, ["loan", "bank details", "ic", "no documents needed"]):
                final_label = "suspicious"
            elif contains_any(lower_text, ["otp", "urgent", "verify"]):
                final_label = "suspicious"

        if final_label == "scam":
            verdict = "⚠️ Scam Detected"
            advice = "Do not click any links, do not reply, and never share OTP, PIN, passwords, IC, or banking details."
        elif final_label == "suspicious":
            verdict = "🧐 Suspicious Message"
            advice = "Be careful. Verify with the official source before taking any action or sharing details."
        else:
            verdict = "✅ Likely Safe"
            advice = "This looks safer, but still stay cautious with links, personal data, and unknown requests."

        ai_explanation = generate_explanation(message, final_label, rule_reasons)

        return jsonify({
            "label": final_label,
            "modelLabel": predicted_label,
            "verdict": verdict,
            "confidence": confidence,
            "advice": advice,
            "aiExplanation": ai_explanation,
            "ruleReasons": rule_reasons,
            "ruleScore": rule_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)