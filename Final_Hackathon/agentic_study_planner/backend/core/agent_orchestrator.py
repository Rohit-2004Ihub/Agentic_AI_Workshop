from backend.agents.topic_extractor import extract_study_topics
from backend.agents.task_scheduler import generate_daily_tasks
from backend.agents.micro_goal_mapper import enrich_tasks_with_micro_goals
from backend.agents.backlog_manager import merge_backlog_into_tasks
from backend.agents.feedback_analyzer import analyze_plan_feedback
from backend.agents.consistency_scorer import calculate_consistency_score

def generate_study_plan(pdf_text, history=[], backlog=[]):
    # Use topic extractor to simulate roadmap if no structured roadmap
    roadmap = extract_study_topics(pdf_text)

    # 🎯 Step 1: Task Scheduler Agent
    tasks = generate_daily_tasks(
        learner_profile="General CS Student",
        roadmap="\n".join(roadmap),
        history="\n".join(history)
    )

    # 🎯 Step 2: Micro Goal Mapper Agent
    enriched = enrich_tasks_with_micro_goals(tasks)

    # 🎯 Step 3: Backlog Manager Agent
    merged = merge_backlog_into_tasks(enriched, backlog)

    # 🎯 Step 4: Feedback Analyzer Agent
    feedback = analyze_plan_feedback(merged)

    # 🎯 Step 5: Consistency Scorer Agent
    consistency = calculate_consistency_score(history, merged)

    return {
        "plan": merged,
        "feedback": feedback,
        "consistency": consistency
    }
