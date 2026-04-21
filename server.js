const express = require("express");
const cors = require("cors");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    message: "NeuraSafe backend is running",
    ai_enabled: false,
    mode: "smart-rule-based",
  });
});

function runRuleAnalysis(message) {
  const text = message.toLowerCase().trim();

  let score = 0;
  const reasons = [];

  if (
    text.includes("urgent") ||
    text.includes("immediately") ||
    text.includes("act now") ||
    text.includes("final warning")
  ) {
    score += 15;
    reasons.push("Uses urgency wording");
  }

  if (
    text.includes("otp") ||
    text.includes("password") ||
    text.includes("pin") ||
    text.includes("verification code")
  ) {
    score += 25;
    reasons.push("Requests sensitive info");
  }

  if (
    text.includes("http") ||
    text.includes("www") ||
    text.includes(".com") ||
    text.includes("bit.ly")
  ) {
    score += 20;
    reasons.push("Contains suspicious link");
  }

  if (
    text.includes("winner") ||
    text.includes("prize") ||
    text.includes("claim now") ||
    text.includes("reward")
  ) {
    score += 15;
    reasons.push("Mentions reward or prize bait");
  }

  if (
    text.includes("bank account") ||
    text.includes("account suspended") ||
    text.includes("verify your account") ||
    text.includes("security alert")
  ) {
    score += 15;
    reasons.push("Pretends to be official account or bank message");
  }

  if (text.includes("!!!")) {
    score += 5;
    reasons.push("Uses excessive punctuation");
  }

  score = Math.min(score, 100);

  let verdict = "";
  let advice = "";

  if (score >= 70) {
    verdict = "⚠️ High Scam Risk";
    advice =
      "Do not click the link, do not reply, and never share OTP or passwords.";
  } else if (score >= 40) {
    verdict = "🧐 Suspicious";
    advice =
      "Please double-check with the official source before doing anything.";
  } else {
    verdict = "✅ Likely Safe";
    advice =
      "This message looks safer, but always stay careful with links and personal info.";
  }

  return {
    score,
    verdict,
    reasons,
    advice,
  };
}

function generateSmartExplanation(message, ruleResult) {
  const explanations = [];

  if (ruleResult.reasons.includes("Uses urgency wording")) {
    explanations.push(
      "This message creates urgency to pressure you into acting quickly without thinking."
    );
  }

  if (ruleResult.reasons.includes("Requests sensitive info")) {
    explanations.push(
      "It asks for sensitive information like OTP, PIN, or password, which scammers use to access accounts."
    );
  }

  if (ruleResult.reasons.includes("Contains suspicious link")) {
    explanations.push(
      "It includes a suspicious link that may lead to a fake website designed to steal your information."
    );
  }

  if (ruleResult.reasons.includes("Mentions reward or prize bait")) {
    explanations.push(
      "It uses reward or prize bait to attract attention and trick users into clicking."
    );
  }

  if (
    ruleResult.reasons.includes("Pretends to be official account or bank message")
  ) {
    explanations.push(
      "It may be impersonating a trusted organization like a bank or service provider to gain your trust."
    );
  }

  if (ruleResult.reasons.includes("Uses excessive punctuation")) {
    explanations.push(
      "It uses excessive punctuation to create panic or force a fast emotional reaction."
    );
  }

  if (explanations.length === 0) {
    return "This message does not show strong scam patterns, but users should still be cautious with unknown senders, links, and requests for personal information.";
  }

  return explanations.join(" ");
}

app.post("/analyze", (req, res) => {
  try {
    const { message } = req.body;

    if (!message || typeof message !== "string" || !message.trim()) {
      return res.status(400).json({
        error: "Message is required",
      });
    }

    const ruleResult = runRuleAnalysis(message);
    const aiExplanation = generateSmartExplanation(message, ruleResult);

    return res.json({
      score: ruleResult.score,
      verdict: ruleResult.verdict,
      reasons: ruleResult.reasons,
      advice: ruleResult.advice,
      aiExplanation: aiExplanation,
    });
  } catch (error) {
    console.error("Analyze error:", error.message);

    return res.status(500).json({
      error: error.message || "Internal server error",
    });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`NeuraSafe backend running on http://0.0.0.0:${PORT}`);
});