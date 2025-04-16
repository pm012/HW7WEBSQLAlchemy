import argparse
from db_model import Student, Teacher, Group, Subject, Grade, Base
from db_init import session


def create_object(model_name, **kwargs):
    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        print(f"Unknown model: {model_name}")
        return
    
    obj = model_class(**kwargs)
    session.add(obj)
    session.commit()
    print(f"{model_name} created with ID: {obj.id}")
    
def list_objects(model_name):
    model_class = MODEL_MAP.get(model_name)
    if not model_class:
        print(f"Unknown model: {model_name}")
        return

    results = session.query(model_class).all()
    for item in results:
        print(item.__dict__)
        
def update_object(model_name, id, **kwargs):
    model_class = MODEL_MAP.get(model_name)
    obj = session.get(model_class, id)
    
    if not obj:
        print(f"{model_name} with ID {id} not found")
        return
    
    for key, value in kwargs.items():
        if key in model_class.__table__.columns:
            setattr(obj, key, value)
        else:
            print(f"Warning: {model_name} has no attribute '{key}' — skipped")

    session.commit()
    print(f"{model_name} with ID {id} has been updated")
    
def remove_object(model_name,id,  **kwargs):
    model_class = MODEL_MAP.get(model_name)
    obj = session.get(model_class, id)
    if not obj:
        print(f"{model_name} with ID {id} not found")
        return
    
    session.delete(obj)
    session.commit()
    print(f"{model_name} with ID {id} removed")
    
def crud_handler(action, model, id_value, clean_data):
    if action == 'create':
        create_object(model, **clean_data)
    elif action == 'list':
        list_objects(model)
    elif action == 'update':
        if not id_value:
            print("Id id required for update")
        else:
            update_object(model, id_value, **clean_data)
    elif action == 'remove':
        if not id_value:
            print("ID is required for removal")
        else: 
            remove_object(model, id_value)
            
def validate_required_fields(model, action, clean_data):
    required_fields_map = {
        'Group': ['group_code', 'group_name'],
        'Student': ['name', 'group_id'],
        'Teacher': ['name'],
        'Subject': ['subj_name', 'teacher_id'],
        'Grade': ['student_id', 'subject_id', 'grade', 'date'],
    }

    if action == 'create':
        missing = []
        for field in required_fields_map.get(model, []):
            if field not in clean_data:
                missing.append(field)
        if missing:
            print(f"Missing required fields for {model}: {', '.join(missing)}")
            exit(1)
            
def get_args():
    parser = argparse.ArgumentParser(description="CLI for managing database models")
    parser.add_argument("-a", "--action", required=True, choices=["create", "list", "update", "remove"], help="Action to perform")
    parser.add_argument("-m", "--model", required=True, help="Model to operate on (Teacher, Student, Group, Subject, Grade)")
    parser.add_argument("-id", "--id", type=int, help="ID of the record (used in update/remove)")
    parser.add_argument("-n", "--name", type=str, help="Generic name field (used for Teacher, Student)")
    
    # Optional fields common to other models
    parser.add_argument("--group_id", type=int)
    parser.add_argument("--group_name", type=str)
    parser.add_argument("--group_code", type=str)

    parser.add_argument("--subj_name", type=str)
    parser.add_argument("--teacher_id", type=int)

    parser.add_argument("--student_id", type=int)
    parser.add_argument("--subject_id", type=int)
    parser.add_argument("--grade", type=int)
    parser.add_argument("--date", type=str)  # string for now, convert to date in code

    return parser.parse_args()
   
    

def main():
    args = get_args()
    model = args.model
    action = args.action
    id_value = args.id

    # Convert Namespace to dict, excluding None values
    clean_data = {k: v for k, v in vars(args).items() if v is not None and k not in ["action", "model", "id"]}

# Map generic `--name` to the model's real field
    if "name" in clean_data:
        if model == "Teacher":
            clean_data["teacher_name"] = clean_data.pop("name")
        elif model == "Student":
            clean_data["name"] = clean_data.pop("name")  # Already correct
        # Add more if needed

    # Optional: convert date string to datetime.date
    from datetime import datetime
    if "date" in clean_data:
        clean_data["date"] = datetime.strptime(clean_data["date"], "%Y-%m-%d").date()

    # Pass to CRUD handler
    crud_handler(action, model, id_value, clean_data)
    session.close()



    
    
    

if __name__ == "__main__":
   
    #Helper: Get model by name
    MODEL_MAP = {
        'Student': Student,
        'Teacher': Teacher,
        'Group': Group,
        'Subject': Subject,
        'Grade': Grade
    }
    main()