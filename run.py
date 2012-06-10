import requests

def pass_changer(accountId, passwd):
	payload = {'accountId': accountId, 'password': passwd, 'id': '', 'command': 'login', 'activeControl': ''}

	s = requests.session()
	print 'Initializing session...',
	r = s.post('https://oam.pdx.edu/idm/user/login.jsp')
	print 'done'

	print 'Logging in...',
	r = s.post('https://oam.pdx.edu/idm/user/login.jsp', data=payload)
	print 'done'
	if 'Welcome to the Odin Account Manager (OAM)' not in r.text:
		print 'Login invalid'
		return
	else:
		print 'Login success'
	return

	for i in range(10):
		tmppass = passwd + str(i)
		print 'Setting pass to %s...' % tmppass,
		payload = {'id': '', 'command': 'Save', 'activeControl': '', 'policyAcceptance': 'true', 'resourceAccounts.password': tmppass, 'resourceAccounts.confirmPassword': tmppass}
		r = s.post('https://oam.pdx.edu/idm/user/changePassword.jsp', data=payload)
		print 'done'
		print r.text
		return


	print 'Setting pass to %s...' % passwd,
	payload = {'id': '', 'command': 'Save', 'activeControl': '', 'policyAcceptance': 'true', 'resourceAccounts.password': passwd, 'resourceAccounts.confirmPassword': passwd}
	r = s.post('https://oam.pdx.edu/idm/user/changePassword.jsp', data=payload)
	print 'done'

if __name__=='__main__':
	username = raw_input('Please enter your username or account ID: ')
	passwd = raw_input('Please enter your password: ')
	pass_changer(username, passwd)
