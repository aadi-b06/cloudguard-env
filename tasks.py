def grade_easy_zombie_volumes(final_state) -> float:
    vol2 = next((r for r in final_state if r.id == "vol-02"), None)
    # Start at 0.1 instead of 0.0
    score = 0.1
    if vol2 and vol2.state == "deleted":
        score = 0.9
    return score

def grade_medium_tagging(final_state) -> float:
    i02 = next((r for r in final_state if r.id == "i-02"), None)
    # Never return 1.0 or 0.0
    return 0.9 if (i02 and "Project" in i02.tags) else 0.1

def grade_hard_cost_optimization(final_state) -> float:
    i02 = next((r for r in final_state if r.id == "i-02"), None)
    # Never return 1.0 or 0.0
    return 0.9 if (i02 and i02.state in ["stopped", "terminated"]) else 0.1
