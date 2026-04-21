"""
Projects Routes Blueprint
"""
from flask import Blueprint, render_template, jsonify, request
import logging

from app.api.projects_api import ProjectsAPI

projects_bp = Blueprint('projects', __name__)
projects_api = ProjectsAPI()

logger = logging.getLogger(__name__)


# -----------------------------
# UI ROUTES
# -----------------------------

@projects_bp.route('/')
def index():
    """Projects home page"""
    return render_template(
        'projects.html',
        title='Projects Explorer',
        active_page='projects'
    )


@projects_bp.route('/home')
def projects_home():
    """Alias for projects home (template compatibility)"""
    return index()


# -----------------------------
# API ROUTES
# -----------------------------

@projects_bp.route('/api/projects')
def api_get_projects():
    """Get list of projects with optional filters"""

    try:
        status = request.args.get('status')          # e.g. active, archived
        owner = request.args.get('owner')
        limit = request.args.get('limit', 20, type=int)
        page = request.args.get('page', 1, type=int)

        # basic validation
        if limit > 100:
            return jsonify({
                'success': False,
                'error': 'Limit cannot exceed 100'
            }), 400

        result = projects_api.get_projects(
            status=status,
            owner=owner,
            limit=limit,
            page=page
        )

        return jsonify({
            'success': True,
            'data': result
        })

    except Exception:
        logger.exception("Failed to fetch projects")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@projects_bp.route('/api/projects/search')
def api_search_projects():
    """Search projects by keyword"""

    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter "q" is required'
        }), 400

    try:
        page = request.args.get('page', 1, type=int)

        results = projects_api.search_projects(
            query=query,
            page=page
        )

        return jsonify({
            'success': True,
            'data': results
        })

    except Exception:
        logger.exception("Project search failed")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@projects_bp.route('/api/projects/<project_id>')
def api_get_project(project_id):
    """Get single project details"""

    try:
        project = projects_api.get_project_by_id(project_id)

        if not project:
            return jsonify({
                'success': False,
                'error': 'Project not found'
            }), 404

        return jsonify({
            'success': True,
            'data': project
        })

    except Exception:
        logger.exception(f"Failed to fetch project {project_id}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@projects_bp.route('/api/projects/stats')
def api_project_stats():
    """Get aggregated project statistics"""

    try:
        stats = projects_api.get_project_stats()

        return jsonify({
            'success': True,
            'data': stats
        })

    except Exception:
        logger.exception("Failed to fetch project stats")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500
