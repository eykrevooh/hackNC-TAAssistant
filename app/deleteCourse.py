from allImports import *
from updateCourse import DataUpdate
from app.logic.getAuthUser import AuthorizedUser
from app.logic import databaseInterface


@app.route("/deletecourse/<tid>/<prefix>/<page>", methods=["POST"])
def deletecourse(prefix, tid, page):

    current_page = "/" + request.url.split("/")[-1]

    authorizedUser = AuthorizedUser(prefix)

    # DATA NEEDED FOR MANIPULATION
    tdcolors = 'danger,danger,danger,danger,danger'
    dataUpdateObj = DataUpdate()
    data = request.form
    cid = int(data['cid'])
    # START PROCESSING THE DELETION OF THE COURSE
    course = Course.get(Course.cId == cid)
    # MAKE SURE THE USER HAS THE CORRECT RIGHTS TO DELETE A COURSE
    if authorizedUser.isAuthorized():
        if not databaseInterface.isTermEditable(tid):

            change = CourseChange.select().where(CourseChange.cId == cid)
            # IF THE RECORD ALREADY EXSISTED THEN WE NEED TO UPDATE THE
            # INFORMATION
            if change.exists():
                updateRecord = CourseChange.get(CourseChange.cId == cid)
                if updateRecord.changeType == 'create' and not updateRecord.verified:
                    updateRecord.delete_instance()
                else:
                    updateRecord.changeType = cfg["changeType"]["delete"]
                    updateRecord.tdcolors = tdcolors
                    updateRecord.lastEditBy = username
                    updateRecord.save()
            else:
                dataUpdateObj.addCourseChange(
                    course.cId, cfg["changeType"]['delete'])
        instructors = InstructorCourseChange.select().where(
            InstructorCourseChange.course == cid)
        for instructor in instructors:
            instructor.delete_instance()
        course.delete_instance()

    flash("Course has been successfully deleted")

    if page == 'courses':
        return redirect(url_for("courses", tID=tid, prefix=prefix))
    else:
        url = "courseManagement/" + page + "/" + tid
        return redirect(url)
