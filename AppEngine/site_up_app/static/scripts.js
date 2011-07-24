function showonlyone(thechosenone){
	var newboxes = document.getElementsByTagName("div");
	for(var x=0; x<newboxes.length; x++){
		name = newboxes[x].getAttribute("class");
		if (name == 'hidden'){
			if (newboxes[x].style.display == 'block'){
				newboxes[x].style.display = 'none';
			}
			else{
				newboxes[x].style.display = 'block';
			}
		}
	}
}

function areyousure(){
	if (confirm('Are you sure?'))
		return true;
	return false;
}