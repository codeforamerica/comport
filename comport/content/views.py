# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for, request, abort
from flask_login import current_user
from flask.ext.login import login_required
from urllib.parse import urlparse
from comport.content.models import ChartBlock
from comport.database import db

blueprint = Blueprint("content", __name__, url_prefix='/content',
                      static_folder="../static")

@blueprint.route("/<int:department_id>", methods=["POST"])
@login_required
def edit_page(department_id):
    if not current_user.has_department(department_id) and not current_user.is_admin():
        abort(401)

    # Importing this at the top of file caused a circular dependency
    # issue so we do a delayed import here
    from comport.department.models import Department
    department = Department.query.filter_by(id=department_id).first()

    # let's sort the contents of the form submission
    changes = {}
    for formfield in request.form:
        # formfield = 'chart_order-pursuits-schema-field-dui-arrest'
        value_name, slug = formfield.split("-", 1)
        if slug not in changes:
            changes[slug] = {}

        changes[slug][value_name] = request.form[formfield]

    for chart_slug in changes:
        block = ChartBlock.query.filter_by(department_id=department_id, slug=chart_slug).first()

        if not block:
            abort(404)

        # set values if they were passed
        block.title = changes[chart_slug]["chart_title"] if "chart_title" in changes[chart_slug] and changes[chart_slug]["chart_title"] else block.title
        block.content = changes[chart_slug]["chart_content"] if "chart_content" in changes[chart_slug] and changes[chart_slug]["chart_content"] else block.content

        if ("chart_order" in changes[chart_slug] and changes[chart_slug]["chart_order"]):
                try:
                    int(changes[chart_slug]["chart_order"])
                except:
                    pass
                else:
                    block.order = int(changes[chart_slug]["chart_order"])

        db.session.add(block)
        # block.save()

        if "blocks_prefix" in changes[chart_slug]:
            blocks = department.get_blocks_by_slug_startswith(changes[chart_slug]["blocks_prefix"])

            block.order = max(min(block.order, len(blocks) - 1), 0)
            db.session.add(block)
            # block.save()

            # Init new array to length of blocks
            new_blocks = [None] * len(blocks)

            # Put block of interest where it's supposed to be
            new_blocks[block.order] = block
            blocks.pop(blocks.index(block))

            # Iterate through new_blocks
            for index, value in enumerate(new_blocks):
                if value is not None:
                    continue

                move_block = blocks.pop(0)
                move_block.order = index
                db.session.add(move_block)
                # move_block.save()
                new_blocks[index] = move_block

    db.session.commit()

    if request.referrer and 'edit' in request.referrer:
        new_path = urlparse(request.referrer.replace('/edit/', '/preview/')).path
    else:
        new_path = url_for(
            'department.department_dashboard', department_id=department_id
        )

    return redirect(new_path)

@blueprint.route("/<string:chart_slug>/<int:department_id>", methods=["POST"])
@login_required
def edit_chart_block(department_id, chart_slug):
    block = ChartBlock.query.filter_by(department_id=department_id, slug=chart_slug).first()

    if not block:
        abort(404)

    if not current_user.has_department(department_id) and not current_user.is_admin():
        abort(401)

    # set values if they were passed
    block.title = request.form["chart_title"] if "chart_title" in request.form and request.form["chart_title"] else block.title
    block.content = request.form["chart_content"] if "chart_content" in request.form and request.form["chart_content"] else block.content

    if ("chart_order" in request.form and request.form["chart_order"]):
            try:
                int(request.form["chart_order"])
            except:
                pass
            else:
                block.order = request.form["chart_order"]

    block.save()

    if "blocks_prefix" in request.form:
        # Importing this at the top of file caused a circular dependency
        # issue so we do a delayed import here
        from comport.department.models import Department
        department = Department.query.filter_by(id=department_id).first()
        blocks = department.get_blocks_by_slug_startswith(request.form["blocks_prefix"])

        block.order = max(min(block.order, len(blocks) - 1), 0)
        block.save()

        # Init new array to length of blocks
        new_blocks = [None] * len(blocks)

        # Put block of interest where it's supposed to be
        new_blocks[block.order] = block
        blocks.pop(blocks.index(block))

        # Iterate through new_blocks
        for index, value in enumerate(new_blocks):
            if value is not None:
                continue

            move_block = blocks.pop(0)
            move_block.order = index
            move_block.save()
            new_blocks[index] = move_block

    if request.referrer and 'edit' in request.referrer:
        new_path = urlparse(request.referrer.replace('/edit/', '/preview/')).path
    else:
        new_path = url_for(
            'department.department_dashboard', department_id=department_id
        )

    return redirect(new_path)
