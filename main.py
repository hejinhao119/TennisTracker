import uuid
from tempfile import NamedTemporaryFile

import streamlit as st

from agents.orchestration import run_coaching_analysis
from evidence.builder import build_evidence
from memory.models import SessionMetric, UserFeedback
from memory.repository import SessionRepository
from memory.session_history import compare_metric


st.set_page_config(page_title="TennisTracker Coach", layout="wide")
st.title("TennisTracker Coach")
st.caption("Evidence-grounded tennis analysis with explicit uncertainty.")

with st.sidebar:
	st.header("Session")
	uploaded_video = st.file_uploader("Upload a match video", type=["mp4", "mov", "avi", "mkv"])
	analyze = st.button("Analyze session", type="primary", disabled=uploaded_video is None)

if analyze and uploaded_video is not None:
	from video_analysis.session_analyzer import analyze_video

	with NamedTemporaryFile(suffix=".mp4", delete=False) as video_file:
		video_file.write(uploaded_video.getbuffer())
		video_path = video_file.name
	try:
		with st.spinner("Extracting frame-level pose evidence..."):
			video_result = analyze_video(video_path)
		evidence = build_evidence(
			session_id=str(uuid.uuid4()),
			strokes=[],
			pose_observations=list(video_result.pose_observations),
		)
		repository = SessionRepository()
		pose_metric = evidence.item("metric.pose.detection_rate")
		previous_pose = repository.get_metric_history(pose_metric.evidence_id, limit=1)
		repository.save_evidence(evidence)
		st.session_state["analysis"] = run_coaching_analysis(evidence)
		st.session_state["evidence"] = evidence
		st.session_state["video_result"] = video_result
		st.session_state["video_name"] = uploaded_video.name
		st.session_state["previous_pose"] = previous_pose[0] if previous_pose else None
	except (OSError, ValueError, RuntimeError) as error:
		st.error(f"Video analysis failed: {error}")

analysis = st.session_state.get("analysis")
if analysis is None:
	st.info("Upload a video to begin a traceable coaching session.")
else:
	st.success(f"Session analyzed: {st.session_state['video_name']}")
	video_result = st.session_state["video_result"]
	evidence = st.session_state["evidence"]
	st.metric("Sampled pose frames", len(video_result.pose_observations))
	st.metric("Pose detection rate", f"{evidence.item('metric.pose.detection_rate').value:.0%}")
	previous_pose = st.session_state.get("previous_pose")
	if previous_pose is not None:
		current_pose = evidence.item("metric.pose.detection_rate")
		comparison = compare_metric(
			previous_pose,
			SessionMetric(
				evidence.session_id,
				current_pose.evidence_id,
				current_pose.value,
				current_pose.sample_count,
				current_pose.measurement_confidence,
			),
		)
		st.caption(f"Previous session change: {comparison.change:+.0%} ({comparison.reason})")
	overview, technical, tactical, trace = st.tabs(
		["Match Overview", "Technical Analysis", "Tactical Analysis", "Agent Trace"]
	)
	with overview:
		st.subheader("Match analysis")
		st.write(analysis.match.summary)
		for limitation in analysis.match.limitations:
			st.warning(limitation)
	with technical:
		st.subheader("Biomechanics")
		st.write(analysis.biomechanics.summary)
		for limitation in analysis.biomechanics.limitations:
			st.warning(limitation)
	with tactical:
		st.subheader("Tactical analysis")
		st.write(analysis.tactical.summary)
		for limitation in analysis.tactical.limitations:
			st.warning(limitation)
	with trace:
		st.subheader("Execution trace")
		st.json({
			"status": "complete",
			"agents": [analysis.match.agent_name, analysis.biomechanics.agent_name,
						analysis.tactical.agent_name, "CoachAgent", "CoachCriticAgent"],
			"attempts": analysis.attempts,
			"critic_approved": analysis.critic.approved,
		})

	st.subheader("Coach report")
	st.write(analysis.coach.diagnosis)
	if analysis.coach.recommendations:
		for recommendation in analysis.coach.recommendations:
			with st.expander(f"Priority {recommendation.priority}: {recommendation.issue}"):
				st.write(recommendation.rationale)
				st.write(f"Drill: {recommendation.drill}")
				st.write(f"Schedule: {recommendation.frequency}; {recommendation.volume}")
				st.write(f"Confidence: {recommendation.confidence:.0%}")
				st.write(f"Evidence: {', '.join(recommendation.evidence_refs)}")
	else:
		for limitation in analysis.coach.limitations:
			st.warning(limitation)

	st.divider()
	st.subheader("Feedback")
	feedback_subject = "coach_report"
	feedback = st.radio("Was this finding useful?", ["Yes", "No"], horizontal=True)
	if st.button("Save feedback"):
		SessionRepository().save_feedback(
			UserFeedback(evidence.session_id, feedback_subject, feedback)
		)
		st.success("Feedback saved for future coaching context.")

