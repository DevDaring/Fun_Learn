"""
Scoring Service
Calculates XP, levels, streaks, and updates user scores
"""

import math
from typing import Any, Optional
from datetime import datetime, timedelta

from app.database.csv_handler import (
    get_users_handler,
    get_sessions_handler,
    get_scores_handler,
    get_teams_handler,
    get_tournaments_handler
)


class ScoringService:
    """
    Service for managing scoring, XP, levels, and streaks.

    Responsibilities:
    - Calculate XP earned from sessions
    - Update user levels based on XP
    - Track and update streaks
    - Calculate team scores
    - Update tournament rankings
    - Generate leaderboards
    """

    def __init__(self):
        """Initialize the scoring service."""
        self.users_handler = get_users_handler()
        self.sessions_handler = get_sessions_handler()
        self.scores_handler = get_scores_handler()
        self.teams_handler = get_teams_handler()
        self.tournaments_handler = get_tournaments_handler()

        # XP calculation constants
        self.BASE_XP_PER_QUESTION = 50
        self.DIFFICULTY_MULTIPLIER = 1.2
        self.COMPLETION_BONUS = 100
        self.STREAK_BONUS_MULTIPLIER = 0.1
        self.PERFECT_SCORE_BONUS = 200

    def calculate_session_xp(
        self,
        session_id: str,
        difficulty_level: int,
        total_questions: int,
        correct_answers: int,
        completion_time_minutes: int,
        is_completed: bool = True
    ) -> dict[str, Any]:
        """
        Calculate XP earned from a session.

        Args:
            session_id: Session identifier
            difficulty_level: Difficulty level (1-10)
            total_questions: Total questions in session
            correct_answers: Number of correct answers
            completion_time_minutes: Time taken to complete
            is_completed: Whether session was completed

        Returns:
            Dictionary with XP breakdown
        """
        try:
            # Base XP from questions
            base_xp = self.BASE_XP_PER_QUESTION * correct_answers

            # Difficulty multiplier
            difficulty_bonus = int(base_xp * (difficulty_level / 10) * self.DIFFICULTY_MULTIPLIER)

            # Completion bonus
            completion_bonus = self.COMPLETION_BONUS if is_completed else 0

            # Perfect score bonus
            perfect_bonus = 0
            if total_questions > 0 and correct_answers == total_questions:
                perfect_bonus = self.PERFECT_SCORE_BONUS

            # Speed bonus (bonus for completing under expected time)
            expected_time = total_questions * 2  # 2 minutes per question expected
            speed_bonus = 0
            if completion_time_minutes < expected_time:
                speed_bonus = int(50 * (expected_time - completion_time_minutes) / expected_time)

            # Total XP
            total_xp = base_xp + difficulty_bonus + completion_bonus + perfect_bonus + speed_bonus

            return {
                "session_id": session_id,
                "base_xp": base_xp,
                "difficulty_bonus": difficulty_bonus,
                "completion_bonus": completion_bonus,
                "perfect_score_bonus": perfect_bonus,
                "speed_bonus": speed_bonus,
                "total_xp": total_xp,
                "breakdown": {
                    "correct_answers": correct_answers,
                    "total_questions": total_questions,
                    "difficulty_level": difficulty_level,
                    "completion_time": completion_time_minutes
                }
            }

        except Exception as e:
            print(f"Error calculating session XP: {e}")
            return {
                "session_id": session_id,
                "total_xp": 0,
                "error": str(e)
            }

    def award_session_xp(
        self,
        user_id: str,
        session_id: str,
        xp_earned: int
    ) -> dict[str, Any]:
        """
        Award XP to user and update level.

        Args:
            user_id: User identifier
            session_id: Session identifier
            xp_earned: XP to award

        Returns:
            Updated user stats
        """
        try:
            user = self.users_handler.find_one({"user_id": user_id})
            if not user:
                raise ValueError(f"User {user_id} not found")

            current_xp = user.get("xp_points", 0)
            current_level = user.get("level", 1)

            # Add XP
            new_xp = current_xp + xp_earned

            # Calculate new level
            new_level = self._calculate_level(new_xp)
            level_up = new_level > current_level

            # Update user
            updates = {
                "xp_points": new_xp,
                "level": new_level
            }

            self.users_handler.update({"user_id": user_id}, updates)

            # Update streak
            streak_info = self.update_streak(user_id)

            return {
                "user_id": user_id,
                "xp_earned": xp_earned,
                "previous_xp": current_xp,
                "new_xp": new_xp,
                "previous_level": current_level,
                "new_level": new_level,
                "level_up": level_up,
                "current_streak": streak_info.get("streak_days", 0),
                "xp_to_next_level": self._xp_for_level(new_level + 1) - new_xp
            }

        except Exception as e:
            print(f"Error awarding XP: {e}")
            return {
                "user_id": user_id,
                "error": str(e)
            }

    def _calculate_level(self, total_xp: int) -> int:
        """
        Calculate level based on total XP.

        Uses formula: level = floor(sqrt(xp / 100)) + 1
        This gives a smooth progression curve.

        Args:
            total_xp: Total XP points

        Returns:
            Level number (1-100)
        """
        if total_xp <= 0:
            return 1

        level = math.floor(math.sqrt(total_xp / 100)) + 1
        return min(level, 100)  # Cap at level 100

    def _xp_for_level(self, level: int) -> int:
        """
        Calculate XP required to reach a level.

        Args:
            level: Target level

        Returns:
            XP required
        """
        if level <= 1:
            return 0

        return ((level - 1) ** 2) * 100

    def update_streak(self, user_id: str) -> dict[str, Any]:
        """
        Update user's learning streak.

        Args:
            user_id: User identifier

        Returns:
            Streak information
        """
        try:
            user = self.users_handler.find_one({"user_id": user_id})
            if not user:
                raise ValueError(f"User {user_id} not found")

            current_streak = user.get("streak_days", 0)
            last_login_str = user.get("last_login", "")

            # Parse last login
            if last_login_str:
                try:
                    last_login = datetime.fromisoformat(last_login_str.replace("Z", "+00:00"))
                except:
                    last_login = datetime.now() - timedelta(days=2)
            else:
                last_login = datetime.now() - timedelta(days=2)

            today = datetime.now().date()
            last_login_date = last_login.date()

            # Check if consecutive day
            days_diff = (today - last_login_date).days

            if days_diff == 0:
                # Same day, no change
                new_streak = current_streak
            elif days_diff == 1:
                # Consecutive day, increment streak
                new_streak = current_streak + 1
            else:
                # Streak broken, reset to 1
                new_streak = 1

            # Update user
            updates = {
                "streak_days": new_streak,
                "last_login": datetime.now().isoformat()
            }

            self.users_handler.update({"user_id": user_id}, updates)

            # Calculate streak bonus XP
            streak_bonus_xp = int(self.BASE_XP_PER_QUESTION * new_streak * self.STREAK_BONUS_MULTIPLIER)

            return {
                "user_id": user_id,
                "streak_days": new_streak,
                "streak_bonus_xp": streak_bonus_xp,
                "streak_status": "maintained" if days_diff <= 1 else "broken"
            }

        except Exception as e:
            print(f"Error updating streak: {e}")
            return {
                "user_id": user_id,
                "streak_days": 0,
                "error": str(e)
            }

    def update_team_score(
        self,
        team_id: str,
        points_to_add: int
    ) -> dict[str, Any]:
        """
        Update team total score.

        Args:
            team_id: Team identifier
            points_to_add: Points to add

        Returns:
            Updated team info
        """
        try:
            team = self.teams_handler.find_one({"team_id": team_id})
            if not team:
                raise ValueError(f"Team {team_id} not found")

            current_score = team.get("total_score", 0)
            new_score = current_score + points_to_add

            self.teams_handler.update(
                {"team_id": team_id},
                {"total_score": new_score}
            )

            return {
                "team_id": team_id,
                "previous_score": current_score,
                "new_score": new_score,
                "points_added": points_to_add
            }

        except Exception as e:
            print(f"Error updating team score: {e}")
            return {
                "team_id": team_id,
                "error": str(e)
            }

    def get_global_leaderboard(
        self,
        limit: int = 100,
        scope: str = "global"
    ) -> list[dict[str, Any]]:
        """
        Get global leaderboard.

        Args:
            limit: Number of entries to return
            scope: Leaderboard scope (global/weekly/monthly)

        Returns:
            List of leaderboard entries
        """
        try:
            users = self.users_handler.find()

            # Sort by XP points
            users.sort(key=lambda x: x.get("xp_points", 0), reverse=True)

            leaderboard = []
            for rank, user in enumerate(users[:limit], 1):
                leaderboard.append({
                    "rank": rank,
                    "user_id": user.get("user_id", ""),
                    "username": user.get("username", ""),
                    "display_name": user.get("display_name", ""),
                    "xp_points": user.get("xp_points", 0),
                    "level": user.get("level", 1),
                    "avatar_id": user.get("avatar_id"),
                    "streak_days": user.get("streak_days", 0)
                })

            return leaderboard

        except Exception as e:
            print(f"Error getting leaderboard: {e}")
            return []

    def get_team_leaderboard(
        self,
        limit: int = 100,
        tournament_id: Optional[str] = None
    ) -> list[dict[str, Any]]:
        """
        Get team leaderboard.

        Args:
            limit: Number of entries to return
            tournament_id: Filter by tournament (optional)

        Returns:
            List of team leaderboard entries
        """
        try:
            if tournament_id:
                teams = self.teams_handler.find({"tournament_id": tournament_id})
            else:
                teams = self.teams_handler.find()

            # Sort by total score
            teams.sort(key=lambda x: x.get("total_score", 0), reverse=True)

            leaderboard = []
            for rank, team in enumerate(teams[:limit], 1):
                leaderboard.append({
                    "rank": rank,
                    "team_id": team.get("team_id", ""),
                    "team_name": team.get("team_name", ""),
                    "total_score": team.get("total_score", 0),
                    "members_count": team.get("current_members", 0),
                    "leader_id": team.get("created_by", "")
                })

            return leaderboard

        except Exception as e:
            print(f"Error getting team leaderboard: {e}")
            return []

    def get_user_stats(self, user_id: str) -> dict[str, Any]:
        """
        Get comprehensive user statistics.

        Args:
            user_id: User identifier

        Returns:
            User statistics dictionary
        """
        try:
            user = self.users_handler.find_one({"user_id": user_id})
            if not user:
                raise ValueError(f"User {user_id} not found")

            # Get all sessions
            sessions = self.sessions_handler.find({"user_id": user_id})
            total_sessions = len(sessions)
            completed_sessions = len([s for s in sessions if s.get("status") == "completed"])

            # Get all scores
            scores = self.scores_handler.find({"user_id": user_id})
            total_questions = len(scores)
            correct_answers = len([s for s in scores if s.get("is_correct", False)])

            # Calculate accuracy
            accuracy_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0

            # Calculate total time
            total_time = sum(s.get("duration_minutes", 0) for s in completed_sessions)

            # Get favorite topics
            topics = [s.get("topic", "") for s in sessions]
            from collections import Counter
            topic_counts = Counter(topics)
            favorite_topics = [topic for topic, count in topic_counts.most_common(3)]

            return {
                "user_id": user_id,
                "username": user.get("username", ""),
                "display_name": user.get("display_name", ""),
                "xp_points": user.get("xp_points", 0),
                "level": user.get("level", 1),
                "streak_days": user.get("streak_days", 0),
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "total_questions_answered": total_questions,
                "correct_answers": correct_answers,
                "accuracy_rate": round(accuracy_rate, 2),
                "total_time_minutes": total_time,
                "favorite_topics": favorite_topics,
                "xp_to_next_level": self._xp_for_level(user.get("level", 1) + 1) - user.get("xp_points", 0)
            }

        except Exception as e:
            print(f"Error getting user stats: {e}")
            return {
                "user_id": user_id,
                "error": str(e)
            }

    def calculate_session_summary(self, session_id: str) -> dict[str, Any]:
        """
        Calculate comprehensive session summary.

        Args:
            session_id: Session identifier

        Returns:
            Session summary with all statistics
        """
        try:
            session = self.sessions_handler.find_one({"session_id": session_id})
            if not session:
                raise ValueError(f"Session {session_id} not found")

            # Get all answers for session
            answers = self.scores_handler.find({"session_id": session_id})

            total_questions = len(answers)
            correct_answers = len([a for a in answers if a.get("is_correct", False)])
            total_score = session.get("score", 0)

            # Calculate time
            started_at_str = session.get("started_at", "")
            completed_at_str = session.get("completed_at", "")

            if started_at_str and completed_at_str:
                try:
                    started = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
                    completed = datetime.fromisoformat(completed_at_str.replace("Z", "+00:00"))
                    duration_seconds = int((completed - started).total_seconds())
                except:
                    duration_seconds = session.get("duration_minutes", 0) * 60
            else:
                duration_seconds = session.get("duration_minutes", 0) * 60

            # Calculate XP
            xp_info = self.calculate_session_xp(
                session_id=session_id,
                difficulty_level=session.get("difficulty_level", 5),
                total_questions=total_questions,
                correct_answers=correct_answers,
                completion_time_minutes=duration_seconds // 60,
                is_completed=session.get("status") == "completed"
            )

            return {
                "session_id": session_id,
                "user_id": session.get("user_id", ""),
                "topic": session.get("topic", ""),
                "difficulty_level": session.get("difficulty_level", 5),
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "accuracy_rate": round((correct_answers / total_questions * 100) if total_questions > 0 else 0, 2),
                "total_score": total_score,
                "duration_seconds": duration_seconds,
                "xp_earned": xp_info.get("total_xp", 0),
                "xp_breakdown": xp_info,
                "status": session.get("status", ""),
                "completed_at": completed_at_str
            }

        except Exception as e:
            print(f"Error calculating session summary: {e}")
            return {
                "session_id": session_id,
                "error": str(e)
            }
