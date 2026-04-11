def grade_easy_zombie_volumes(final_state) -> float:
    vol1 = next((r for r in final_state if r.id == "vol-01"), None)
    vol2 = next((r for r in final_state if r.id == "vol-02"), None)
    
    score = 0.05
    if vol2 and vol2.state == "deleted":
        score += 0.45
    if vol1 and vol1.state != "deleted":
        score += 0.45
        
    return float(max(0.01, min(0.99, score)))

def grade_medium_tagging(final_state) -> float:
    i02 = next((r for r in final_state if r.id == "i-02"), None)
    if i02 and "Project" in i02.tags:
        return 0.95
    return 0.05

def grade_hard_cost_optimization(final_state) -> float:
    i01 = next((r for r in final_state if r.id == "i-01"), None)
    i02 = next((r for r in final_state if r.id == "i-02"), None)
    
    score = 0.05
    if i02 and i02.state in ["stopped", "terminated"]:
        score += 0.45
    if i01 and i01.state == "running":
        score += 0.45
    return float(max(0.01, min(0.99, score)))
