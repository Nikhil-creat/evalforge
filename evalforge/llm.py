import re
from collections import Counter
from .config import PROVIDER, ANTHROPIC_MODEL, OPENAI_MODEL

def ask(prompt, system="You are a precise ML evaluation assistant."):
    """Returns None in offline (heuristic) mode."""
    if PROVIDER == "anthropic":
        import anthropic
        r = anthropic.Anthropic().messages.create(model=ANTHROPIC_MODEL, max_tokens=300, system=system,
                                                  messages=[{"role": "user", "content": prompt}])
        return r.content[0].text
    if PROVIDER == "openai":
        from openai import OpenAI
        r = OpenAI().chat.completions.create(model=OPENAI_MODEL, messages=[
            {"role": "system", "content": system}, {"role": "user", "content": prompt}])
        return r.choices[0].message.content
    return None

_STOP = set("the a an to of for my i is in on and how do can me this that with your you it what".split())

def label_cluster(prompts):
    out = ask("Give a 2-4 word topic label for these user prompts. Reply with the label only:\n- " + "\n- ".join(prompts[:12]))
    if out:
        return out.strip().strip('"')
    words = Counter(w for p in prompts for w in re.findall(r"[a-z]{3,}", p.lower()) if w not in _STOP)
    return " / ".join(w for w, _ in words.most_common(3))

_BASE = {1: 0.9, 0: 0.6, -1: 0.2}

def score_quality(prompt, response, feedback):
    """Explicit user feedback wins; the LLM only grades unrated interactions."""
    if feedback != 0 or PROVIDER == "heuristic":
        s = _BASE[int(feedback)]
        return s - 0.3 if len(response) < 25 or "not sure" in response.lower() else s
    out = ask(f"Rate the answer quality 0-1. Reply with a number only.\nQ: {prompt}\nA: {response}")
    m = re.search(r"[01](?:\.\d+)?", out or "")
    return float(m.group()) if m else 0.6
