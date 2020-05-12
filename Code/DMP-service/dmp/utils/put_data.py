from dmp.extensions import db


def put_data(rootgroup, obj):
    try:
        if rootgroup.max_count == None:
            rootgroup.max_count = 1
        else:
            rootgroup.max_count += 1
        db.session.add(obj)
        db.session.commit()

    except Exception as e:
        print(e)
        db.session.rollback()