from rolepermissions.roles import AbstractUserRole


class Monitor(AbstractUserRole):
	available_permissions = {
	    'list_especimen' : True,
		'add_especimen' : True,
		}


class Curador(AbstractUserRole):
	available_permissions = {
	    'list_monitor' : True,
		'add_monitor' : True,
		}
		
class Investigador(AbstractUserRole):
	available_permissions = {
	    'list_monitor' : True,
		'add_monitor' : True,
		}
		
class Director(AbstractUserRole):
	available_permissions = {
	    'list_monitor' : True,
		'add_monitor' : True,
		}
