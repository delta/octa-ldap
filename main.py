import ldap
import config
from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/info/<username>')
def getInfo(username):
	try:
		ldap.set_option(ldap.OPT_REFERRALS,0)

		# Open a connection
		l = ldap.initialize("ldap://diamond.octa.edu")
		l.protocol_version = ldap.VERSION3

		# Bind/authenticate with a user with apropriate rights to add objects
		l.simple_bind_s(config.LOGIN_USERNAME+"@octa.edu",config.LOGIN_PASSWORD)

		ldap_base = "dc=octa,dc=edu"
		query = "(cn="+username+")"
		result = l.search_s(ldap_base, ldap.SCOPE_SUBTREE, query)

		returnValue = {}
		facultyInfo = result[0][0]
		details = result[0][1]['description'][0].strip().split('-')
		year    = result[0][1]['mail'][0].strip('@nitt.edu')
		if facultyInfo is None:
			returnValue['success'] = False
			returnValue['name']    = "User doesn't exist"
			returnValue['faculty'] = False
		else:
			returnValue['success'] = True
			name                   = result[0][1]['displayName'][0].strip()
			if 'OU=FACULTY' in facultyInfo:
				returnValue['faculty'] = True
				returnValue['name']    = name
			else:
				returnValue['faculty'] = False
				if year[5] == '4':
					details    = result[0][1]['description'][0].strip().split(' ')
					course = details[0]
					dept   = details[1]
					state  = details[4]
					phone  = details[5]
				if year[5] == '5':
					course = details[0]
					dept   = details[1]
					state  = details[4]
					phone  = details[5]
				if year[5] == '6':
					course = details[0]
					dept   = details[1]
					state  = details[3]
					phone  = details[4]
				if year[5] == '7':
					course = details[0]
					dept   = details[1]
					state  = details[4]
					phone  = details[5]
				if year[5] == '8':
					course = details[0]
					dept   = details[1]
					state  = details[5]
					phone  = result[0][1]['telephoneNumber'][0]

				returnValue['name']        = name
				returnValue['course']      = course
				returnValue['dept']        = dept
				returnValue['state']       = state
				returnValue['phone']       = phone
				returnValue['faculty']     = False
			
		
		# Its nice to the server to disconnect and free resources when done
		l.unbind_s()
		
		
	
		
		return jsonify(returnValue)
	
	except (KeyboardInterrupt, SystemExit):
		raise

	except:
		returnValue = {
			"success": False,
			"faculty": False,
			"name": "An internal error occured"
		}

		return jsonify(returnValue)

if __name__ == '__main__':
	app.run(port=config.PORT)
