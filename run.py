import argparse
import sys

import requests

def set_pass(session, new_pass):
	r = session.post('https://oam.pdx.edu/idm/user/changePassword.jsp', {
			'id': '',
			'command': 'Save',
			'activeControl': '',
			'policyAcceptance': 'true',
			'resourceAccounts.password': new_pass,
			'resourceAccounts.confirmPassword': new_pass })
	if 'AlrtMsgTxt' in r.text:
		raise ValueError('Error setting new password')
	else:
		return r

def pass_changer(accountId, cur_passwd, new_passwd):
	payload = {'accountId': accountId, 'password': cur_passwd, 'id': '', 'command': 'login', 'activeControl': ''}

	s = requests.session()
	print 'Initializing session...',
	sys.stdout.flush()
	r = s.post('https://oam.pdx.edu/idm/user/login.jsp')
	print 'done'

	print 'Logging in...',
	sys.stdout.flush()
	r = s.post('https://oam.pdx.edu/idm/user/login.jsp', data=payload)
	print 'done'
	if 'Welcome to the Odin Account Manager (OAM)' not in r.text:
		print 'Login invalid'
		return
	else:
		print 'Login success'

	if cur_passwd == new_passwd:
		for i in range(10):
			newpass = new_passwd + str(i)
			print 'Setting password to %s ...' % newpass,
			sys.stdout.flush()
			try:
				set_pass(s, new_passwd + str(i))
				print 'done'
			except ValueError:
				print 'Error!'
				return

	print 'Setting password to %s ...' % new_passwd,
	sys.stdout.flush()
	try:
		set_pass(s, new_passwd)
		print 'done'
	except ValueError:
		print 'Error!'

if __name__=='__main__':
	# Arg parsing
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--passwd', dest='passwd',
		help='Current password', required=True)
	parser.add_argument('-u', '--user', dest='user',
		help='Username or account ID', required=True)
	parser.add_argument('-n', '--newpass', dest='newpass',
		help='New password, undefined means reset to original password', required=False)
	args = parser.parse_args()

	if args.newpass:
		newpass = args.newpass
	else:
		newpass = args.passwd
	pass_changer(args.user, args.passwd, newpass)
	
