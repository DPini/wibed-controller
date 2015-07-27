$(document).ready(function(){
	$('#checkAll').on('click',function(){
		if ($(this).is(':checked')) {
			$('.node').each(function(){
				this.checked = true;
			});
		}else{
			$('.node').each(function(){
				this.checked = false;
			});
		}
	})
});
