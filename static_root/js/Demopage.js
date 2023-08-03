
    $(document).ready(function(){


      

        if ( window.history.replaceState ) {
          window.history.replaceState( null, null, window.location.href );

          }
          
         var newdatatable_ip = $("#newdatatable").DataTable();

        var table_ip = $("#datatable").DataTable();
        valuedict = {};
        var i=1;
  
        $(".tableclass").fadeOut(0);    
        $("#exports").hide();

        // $('.user-error').remove();
  
        
        
  
  
        regLast= /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        $('.text-error').remove();
        $('#inputtext').on('keyup', function () {
  
          $('.text-error').remove();
         var ok=true;
          
          // regLast = /^[a-zA-Z]{2,20}$/;
          if (!regLast.test(document.getElementById("inputtext").value))
          {
              ok=false;
              $(this).parent('.form-group').append("<span class='text-error'>Please enter a valid IP.</span>");
          }
  
         
          return ok;
          
          });
  
  
  
          $('.text-error').remove();
          $('#inputtext').on('keyup', function () {
    
            $('.text-error').remove();
           var ok=true;
            
            // regLast = /^[a-zA-Z]{2,20}$/;
            if (!regLast.test(document.getElementById("inputtext").value))
            {
                ok=false;
                $(this).parent('.form-group').append("<span class='text-error'>Please enter a valid IP.</span>");
            }
    
           
            return ok;
            
            });
        $("#btn1").click(function(){
  
  
  
          var ip = document.getElementById('inputtext');
          var device = document.getElementById('device_type');
          var username= document.getElementById('username');
          var password= document.getElementById('password');
          const haskey = valuedict.hasOwnProperty(ip.value) 
  
  
          valuedict[ip.value] = {}
          

          
            // && haskey == false && device.val != "Default" 
          if (ip.value == "" ){
            $('.text-error').remove();
            $('#inputtext').parent('.form-group').append("<span class='text-error'>Input IP is Empty</span>");
            // alert("Input IP is Empty")
            // $("#ipError").html("Input IP is Empty !!").addClass("test-danger");
          
        }
        else if ( !regLast.test(ip.value)){
            
            $('.text-error').remove();
            $('#inputtext').parent('.form-group').append("<span class='text-error'>Please enter a valid IP.</span>");
          }
        else if(device.value == "Default"){
            $('.text-error').remove();
            $('#device_type').parent('.form-group').append("<span class='text-error'>Please Select any option</span>");
        }
        else if(username.value == ""){
            $('.text-error').remove();
            $('#username').parent('.form-group').append("<span class='text-error'>Please Enter the username</span>");
        }
        else if (password.value == ""){
            $('.text-error').remove();
            $('#password').parent('.form-group').append("<span class='text-error'>Please Enter the username</span>");
        }


        else {

            $('.text-error').remove();




            valuedict[ip.value]['device_make'] = device.value;
            valuedict[ip.value]['username'] = username.value;
            valuedict[ip.value]['password'] = password.value;
            
          console.log(ip.value,'ip.value')
          
        //   if( regLast.test(ip.value)){
        //     console.log("yes")
        //   }
    
          
    
    
          $(".tableclass").fadeIn();

          table_ip.row.add([i , ip.value ,  device.value,  username.value, 
            "</td><td><button type='button' class='btn btn-danger'>"+"Delete"+"</button>"]).draw(false);

    
    
          // table_ip.row.add([i , ip.value ,  device.value,  username.value, "</td><td><select >"+"<option value='Inactive' hidden>Choose to Delete</option>"+"<option value='Active' >Delete</option>"+"</select>"]).draw(false);
          i+=1;
          ip.value = "";
          username.value="";
          password.value="";
          $('#device_type option').prop('selected', function(){
            return this.defaultSelected;
          })  
    
    
          $('#datatable').find('tr').click( function(data){
            var myrow = $(this).find('td:eq(1)').text();
            
    
            var removingRow = $(this).closest('tr');
    
            table_ip.row(removingRow).remove().draw();
    

            delete valuedict[myrow]
            console.log(valuedict,'=====after delete')
          });
  
        }


        
  
  
        })
      
  
        $("#deleteAll").click(function() {
          $('#datatable').DataTable().clear().draw();
          valuedict = {};
          });
  
  
        $("#Ipsubmit").click(function(e){   
          e.preventDefault();
          $('.text-error').remove();


          
          // Validation
          var MYACT = document.getElementById('Activity_name');
          if(MYACT.value == "default"){
            $('.text-error').remove();
            $('#Activity_name').parent('.form-group').append("<span class='text-error'>Please Select any option</span>");
          }
          else if (Object.entries(valuedict).length === 0){
            $('.text-error').remove();
            $('#btn1').parent('.form-group').append("<span class='text-error'>Please Add device</span>");
          }
          else{
              $.ajax({
                type:'POST',
                url:loadUrl,
                data:{
                  'valuedict': JSON.stringify(valuedict),
                  'Activity_type': $("#Activity_name").val(),
                  'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                  
                  },
        
                
                  success:function(response){
                    console.log("successfully")

                    var myact= response['Activity_type']

                    var Jdata = response['jsondata']

                    console.log(Jdata,'=========Jdata',typeof(Jdata))

                    document.getElementById('hiddenJson').value = Jdata
                    document.getElementById('myact').value = myact

                    

                    
                    $('#Activity_name option').prop('selected', function(){
                      return this.defaultSelected;
                    })
                    $("#exports").show();
                  },
              })
          }
        })
  
  
  
  
  });
   
  
      
     
