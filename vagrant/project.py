from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def showRestaurants():
	try:
		restaurants = session.query(Restaurant).all()
		return render_template('restaurants.html', restaurants=restaurants)
	except:
		session.rollback()
		raise
	finally:
		session.close()

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
	if request.method == 'POST':
		try:
			newRestaurant = Restaurant(name=request.form['name'])
			session.add(newRestaurant)
			session.commit()
			flash("New Restaurant Created")
			return redirect(url_for('showRestaurants'))
		except:
			session.rollback()
			raise
		finally:
			session.close()
	else:
		return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def editRestaurant(restaurant_id):
	try:
		editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	except:
		session.rollback()
		raise
	finally:
		session.close()
	if request.method == 'POST':
		try:
			editedRestaurant.name = request.form['name']
			session.add(editedRestaurant)
			session.commit()
			flash("Restaurant Successfully Edited")
			return redirect(url_for('showRestaurants'))
		except:
			session.rollback()
			raise
		finally:
			session.close()
	else:
		return render_template('editrestaurant.html', r=editedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
	try:
		deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	except:
		session.rollback()
		raise
	finally:
		session.close()
	if request.method == 'POST':
		try:
			session.delete(deletedRestaurant)
			session.commit()
			flash("Restaurant Successfully Deleted")
			return redirect(url_for('showRestaurants'))
		except:
			session.rollback()
			raise
		finally:
			session.close()
	else:
		return render_template('deleterestaurant.html', r=deletedRestaurant)
	
@app.route('/restaurants/JSON')
def restaurantsJSON():
	try:
		restaurants = session.query(Restaurant).all()
		return jsonify(Restaurants=[r.serialize for r in restaurants])
	except:
		session.rollback()
		raise
	finally:
		session.close()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	try:
		restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
		items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
		return jsonify(MenuItems=[i.serialize for i in items]) 
	except:
		session.rollback()
		raise
	finally:
		session.close()


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
	try:
		item = session.query(MenuItem).filter_by(id=menu_id).one()
		return jsonify(MenuItem=[item.serialize])
	except:
		session.rollback()
		raise
	finally:
		session.close()


@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	try:
		restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
		items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
		count = items.count()
		print("Count is " + str(count))
		return render_template('menu.html', restaurant=restaurant, items=items)
	except:
		session.rollback()
		raise
	finally:
		session.close()

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET','POST']) 	
def newMenuItem(restaurant_id):
        if request.method == 'POST':
		try:
			newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
			session.add(newItem)
			session.commit()
			flash("New Menu Item Created")
			return redirect(url_for('showMenu', restaurant_id=restaurant_id))
		except:
			session.rollback()
			raise
		finally: 
			session.close()
	else:
		return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
	try:
		editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	except:
		session.rollback()
	finally:
		session.close()
	if request.method == 'POST':
		if request.form['name']:
			try:
				editedItem.name = request.form['name']
				session.add(editedItem)
				session.commit()
				flash("Menu Item Successfully Edited")
				return redirect(url_for('showMenu', restaurant_id=restaurant_id))
			except:
				session.rollback()
				raise
			finally:
				session.close()
	else:
		return render_template('editmenuitem.html', i=editedItem)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	try:
		deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	except:
		session.rollback()
	finally:
		session.close()
	if request.method == 'POST':
		try:
			session.delete(deletedItem)
			session.commit()
			flash("Menu Item Successfully Deleted")
			return redirect(url_for('showMenu', restaurant_id=restaurant_id))
		except:
			session.rollback()
			raise
		finally:
			session.close()
	else:
		return render_template('deletemenuitem.html', i=deletedItem)

	return "task 3 complete"


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
