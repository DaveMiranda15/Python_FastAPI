from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# API = Application Programming Interface
# GET POST PUT DELETE
# http://127.0.0.1:8000/docs to check the API page

class Item(BaseModel):
	name: str
	price: float
	flavor: Optional[str] = None

class UpdateItem(BaseModel):
	name: Optional[str] = None
	price: Optional[float] = None
	flavor: Optional[str] = None

inventory = {}

@app.get("/")
def home():
	return {"Data": "Working API."}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item you'd like to view.", gt=0)): # use this to check: http://127.0.0.1:8000/get-item/2
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail="Item ID not found.")
	return inventory[item_id]

# example: "facebook.com/home?redirect=/jun&msg=fail"
@app.get("/get-by-name/{item_id}")
# put * in front of the arguments to aviod error in Python.
# in python, it requires mandatory keywords should be in front of the non-mandatory keywords
# To check: http://127.0.0.1:8000/get-by-name/1?test=0&name=Milk
def get_item(*, item_id = int, name: Optional[str] = None, test: int):
	for item_id in inventory:
		if inventory[item_id].name == name:
			return inventory[item_id]
	raise HTTPException(status_code=404, detail="Item name not found.")

@app.post("/create-item/{item_id}")
def create_item(item: Item, item_id: int = Path(None, description="The ID of the item you'd like to create.", gt=0)):
	if item_id in inventory:
		raise HTTPException(status_code=400, detail="Item ID already exists.")

	#inventory[item_id] = {"name": item.name, "price": item.price, "flavor": item.flavor}
	inventory[item_id] = item
	return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item: UpdateItem, item_id: int = Path(None, description="The ID of the item you'd like to update.", gt=0)):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail="Item ID does not exists.")


	if item.name != None: 
		inventory[item_id].name = item.name

	if item.price != None: 
		inventory[item_id].price = item.price

	if item.flavor != None: 
		inventory[item_id].flavor = item.flavor

	return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete.", gt=0)):
	if item_id not in inventory:
		raise HTTPException(status_code=404, detail="Item ID does not exists.")

	del inventory[item_id]
	return {"Success": "Item deleted!"}
