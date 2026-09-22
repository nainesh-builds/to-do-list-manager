import os
from supabase import create_client, Client
from to_do import To_do

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def load_todos():
    final_list = []
    response = supabase.table("to_do").select("*").execute()
    print(response)
    #response.data = [{'id': '83c219ea', 'title': 'Docker', 'description': 'Run Containers', 'created_at': '2026-09-20T21:29:20.949322+00:00'}]
    for item in response.data:
        id = item['id']
        title = item['title']
        description = item['description']
        task = To_do(task_id=id, title=title, desc=description)
        final_list.append(task)  

    return final_list

def create_to_do(task : To_do):
    try:
        # Step 1 - Extract id, title, desc
        id = task.get_id()
        title = task.get_title()
        description = task.get_desc()
        # Step 2 - Create a to_do item in to_do table
        response = supabase.table("to_do").insert({"id" : id, "title" : title, "description" : description}).execute()
        # Step 3 - Get timestamp from newly added to_do item
        timestamp = response.data[0]['created_at']
        # Step 4 - Return status and timestamp
        status = True
    except:
        status = False
        timestamp = ''
    return status, timestamp


def edit_one_item(task):

    id = task.get_id()
    title = task.get_title()
    description = task.get_desc()
    
    response = (supabase.table("to_do").update({"title": title, "description": description}).eq("id", id).execute())

    return response.data[0]

def delete_item(task):
    try:
        id = task.get_id()       
        response = supabase.table("to_do").delete().eq("id", id).execute()
        status = True
    except:
        status = False
    return status