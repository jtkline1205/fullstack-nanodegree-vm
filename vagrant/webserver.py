from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
	 
html_start = "<html><body>"
html_end = "</body></html>"
success_code = 200
 
def send_success(self):
                self.send_response(success_code)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

class webserverHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path.endswith("/restaurants"):
				send_success(self)
				output = ""
				output += html_start
				output += "<a href='/restaurants/new'>Create A New Restaurant Here</a><br/><br/>"
				restaurants = session.query(Restaurant).all()
				for restaurant in restaurants:
					output += (restaurant.name + "<br/>")
					output += "<a href='/%s/edit'>Edit</a><br/><a href='/%s/delete'>Delete</a><br/><br/>" % (str(restaurant.id), str(restaurant.id))
				output += html_end
				self.wfile.write(output)
				return
			if self.path.endswith("/new"):
				send_success(self)
				output = ""
				output += html_start
				output += "Create a new restaurant"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter restaurant name</h2><input name='new_restaurant_name' type='text'><input type='submit' value='Create'></form>"
				output += html_end
				self.wfile.write(output)
				return
			if self.path.endswith("/edit"):
				send_success(self)
				restaurant_id = self.path.split('/')[1]
				restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
				output = ""
				output += html_start
				output += restaurant.name
				output += "<form method='POST' enctype='multipart/form-data' action='/%s/edit'><input name='edited_restaurant_name' type='text' placeholder='%s'><input type='submit' value='Rename'></form>" % (str(restaurant.id), restaurant.name)
				output += html_end
				self.wfile.write(output)
				return
			if self.path.endswith("/delete"):
				send_success(self)
				restaurant_id = self.path.split('/')[1]
				output = ""
				output += html_start
				output += "<h1>Are you sure you want to delete this restaurant?</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/%s/delete'><input type='submit' value='Delete'></form>" % str(restaurant_id)
				output += html_end
				self.wfile.write(output)
		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)
	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('new_restaurant_name')
				newRestaurant = Restaurant(name=messagecontent[0])
				session.add(newRestaurant)
				session.commit()
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
				return
			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('edited_restaurant_name')
				restaurant_id = self.path.split('/')[1]
				restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
				restaurant.name = messagecontent[0]
				session.add(restaurant)
				session.commit()
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()
			if self.path.endswith("/delete"):
				restaurant_id = self.path.split('/')[1]
				restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
				session.delete(restaurant)
				session.commit()
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurants')
				self.end_headers()

			#if self.path.endswith("/edit"):
				
							

			#self.send_response(301)
			#self.end_headers()

			#ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			#if ctype == 'multipart/form-data':
			#	fields=cgi.parse_multipart(self.rfile, pdict)
			#	message_content = fields.get('message')
			#	if (message_content):
			#		print(message_content[0])
			#	restaurant_name_content = fields.get('restaurant_name')
			#	if (restaurant_name_content):
			#		print(restaurant_name_content[0])
			#output = ""
			#output += html_start
			#if (message_content):
			#	output += " <h2> Okay, how about this: </h2>"
			#	output += "<h1> %s </h1>" % message_content[0]
			#	output += hello_form_html
			#if (restaurant_name_content):
			#	newRestaurant = Restaurant(name = restaurant_name_content[0])
			#	session.add(newRestaurant)
			#	session.commit()
			#	restaurants = session.query(Restaurant).all()
			#	for restaurant in restaurants:
			#		output += restaurant.name
			#		output += restaurant_line_item_html
			#output += html_end

			#self.wfile.write(output)
			#print output
			
		except:
			pass


def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running in port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()


if __name__ == '__main__':
	main()
