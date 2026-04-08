def grade_easy_zombie_volumes(final_state) -> float:
    # Objective: Delete vol-02 (available), keep vol-01 (in-use)
    vol1 = next((r for r in final_state if r.id == "vol-01"), None)
    vol2 = next((r for r in final_state if r.id == "vol-02"), None)
    
    score = 0.0
    if vol2 and vol2.state == "deleted":
        score += 0.5
    if vol1 and vol1.state != "deleted":
        score += 0.5
        
    return score

def grade_medium_tagging(final_state) -> float:
    # Objective: i-02 needs a "Project" tag.
    i02 = next((r for r in final_state if r.id == "i-02"), None)
    if i02 and "Project" in i02.tags:
        return 1.0
    return 0.0

def grade_hard_cost_optimization(final_state) -> float:
    # Objective: i-02 has 2% CPU. Stop or terminate it. Keep i-01 running.
    i01 = next((r for r in final_state if r.id == "i-01"), None)
    i02 = next((r for r in final_state if r.id == "i-02"), None)
    
    score = 0.0
    if i02 and i02.state in ["stopped", "terminated"]:
        score += 0.5
    if i01 and i01.state == "running":
        score += 0.5
    return score