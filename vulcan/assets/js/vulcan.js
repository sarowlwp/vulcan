$(document).ready(function(){
	//alert("hello jquery")
	var origin_html
	
	$("#task_talbe").dataTable();
	$(".alert").alert('close')

	$(".task_unedit > .cancel").on({
		click:function(){
			taskid = $(this).parent().parent().parent().find("td").first().text()
			delete_task(taskid,$(this))
		}
	});
	
	$(".task_unedit > .ok").on({
		click:function(){
			taskid = $(this).parent().parent().parent().find("td").first().text()
			update_task_status(taskid,"1",$(this))
		}
	});
	
	$(".task_unedit > .edit").on({
		click:function(){
			$tr = $(this).parent().parent().parent()
			taskname = $tr.find(".task_unedit:eq(0)").text()
			$tr.find(".task_edit:eq(0)").find(".data-input").val(taskname)
			
			stage = $tr.find(".task_unedit:eq(1)").attr("default-value")
			$tr.find(".task_edit:eq(1)").find(".data-input").val(stage)
			
			user = $tr.find(".task_unedit:eq(2)").attr("default-value")
			$tr.find(".task_edit:eq(2)").find(".data-input").val(user)
			
			priority = $tr.find(".task_unedit:eq(3)").attr("default-value")
			$tr.find(".task_edit:eq(3)").find(".data-input").val(priority)
			
			taskdesc = $tr.find(".task_unedit:eq(4)").text()
			$tr.find(".task_edit:eq(4)").find(".data-input").val(taskdesc)
			
			$tr.find(".task_unedit").hide()
			$tr.find(".task_edit").show()
		}
	});
	
	$(".task_edit > .ok").on({
		click:function(){
			taskid = $(this).parent().parent().parent().find("td").first().text()
			$tr = $(this).parent().parent().parent()
			taskname = $tr.find("td:eq(1)").find(".data-input").val()
			stageid = $tr.find("td:eq(2)").find(".data-input").val()
			userid = $tr.find("td:eq(3)").find(".data-input").val()
			priority = $tr.find("td:eq(4)").find(".data-input").val()
			taskdescription = $tr.find("td:eq(6)").find(".data-input").val()
			update_task_all(taskid,taskname,stageid,userid,priority,taskdescription)
		}
	});
	
	$(".task_edit > .cancel").on({
		click:function(){
			$tr = $(this).parent().parent().parent()
			$tr.find(".task_unedit").show()
			$tr.find(".task_edit").hide()
			
		}
	});
	
	$(".add_task").on({
		click:function(){
			$("#task_add_table").show()
		}
	});
	
	$("#task_add_table > tbody > tr > td").last().find("a:eq(1)").on({
		click:function(){
			$("#task_add_table").hide()
		}
	});
	
	$("#task_add_table > tbody > tr > td").last().find("a:eq(0)").on({
		click:function(){
			taskname = $("#task_add_table > tbody > tr > td:eq(0)").find(".data-input").val()
			stageid = $("#task_add_table > tbody > tr > td:eq(1)").find(".data-input").val()
			userid = $("#task_add_table > tbody > tr > td:eq(2)").find(".data-input").val()
			priority = $("#task_add_table > tbody > tr > td:eq(3)").find(".data-input").val()
			endtime = $("#task_add_table > tbody > tr > td:eq(4)").find(".data-input").val()
			taskdescription = $("#task_add_table > tbody > tr > td:eq(5)").find(".data-input").val()
			//alert(taskname + stageid + userid + priority + end_time + description)
			add_task(taskname,stageid,userid,priority,endtime,taskdescription)
		}
	});
	
	var td_check = false
	// $("#task_table > tbody > tr > td").on({
// 	
		// dblclick:function(){
			// $(this).find(".task_unedit").hide()
			// value = $(this).find(".task_unedit").text()
			// $(this).find(".task_edit").find(".data-input").val(value)
			// $(this).find(".task_edit").show()
			// td_check = true
		// },
		// mouseleave:function(){
			// if(td_check === true){
				// $unedit = $(this).find(".task_unedit")
				// $edit = $(this).find(".task_edit")
				// new_value = $edit.find(".data-input").val()
				// taskid = $(this).parent().find("td").first().text()
				// filed = $(this).attr("filed")
				// if(new_value != "" && new_value != $unedit.text()){
					// update_task(taskid,filed,new_value,$(this))
				// }
				// $unedit.show()
				// $edit.hide()
				// td_check = false
			// }
		// }
	// });
	
	update_task_status = function(taskid,value,$button){
		$.ajax({
			type:"post",
			url:"/task/"+taskid,
			dataType:"json",
			data:{
				_method:"put",
				status:value
			},
			success:function(data,code){
				if(data.code === 200){
					$button.parent().parent().parent().remove()
				}else{
					alert("update error")
				}
			},
			error:function(){
				
			}
		});
		
	}
		
	
	update_task = function(taskid,filed,value,$td){
		$unedit = $td.find(".task_unedit")
		$edit = $td.find(".task_edit")
		un_params = "{_method:\"put\","
		+ filed + ":\"" + value +"\"}"
		eval('var params = ' + un_params); 
		$.ajax({
			type:"post",
			url:"/task/"+taskid,
			dataType:"json",
			data:params,
			success:function(data,code){
				//alert(data.code)
				//alert(code)
				if(data.code === 200){
					if(filed === "userid" || filed === "priority"){
						$unedit.text($edit.find("option:selected").text())
					}else if(filed === "stageid"){
						location.reload()
					}else{
						$unedit.text(value)
					}
				}else{
					alert("update error")
				}
			},
			error:function(){
				
			}
		});
	}
	
	delete_task = function(taskid,$button){
		$.ajax({
			type:"post",
			url:"/task/"+taskid,
			dataType:"json",
			data:{
				_method:"delete"
			},
			success:function(data,code){
				if(data.code === 200){
					$button.parent().parent().parent().remove()
				}else{
					alert("update error")
				}
			},
			error:function(){
				
			}
		});
	}
	
	add_task = function(taskname,stageid,userid,priority,endtime,taskdescription){
		$.ajax({
			type:"post",
			url:"/task/",
			dataType:"json",
			data:{
				taskname:taskname,
				stageid:stageid,
				userid:userid,
				priority:priority,
				endtime:endtime,
				taskdescription:taskdescription
			},
			success:function(data,code){
				if(data.code === 200){
					location.reload()
				}else{
					alert("add error")
				}
			},
			error:function(){
				
			}
		});
		
	}
	
	update_task_all = function(taskid,taskname,stageid,userid,priority,taskdescription){
		$.ajax({
			type:"post",
			url:"/task/"+taskid,
			dataType:"json",
			data:{
				_method:"put",
				taskname:taskname,
				stageid:stageid,
				userid:userid,
				priority:priority,
				taskdescription:taskdescription
			},
			success:function(data,code){
				if(data.code === 200){
					location.reload()
				}else{
					alert("add error")
				}
			},
			error:function(){
				
			}
		});
		
	}
});


