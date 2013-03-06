;$verb($jsonserver, "logincmd_guest", $god)
program $jsonserver:logincmd_guest
	$private();
	
	return $guest:create_guest();
.
