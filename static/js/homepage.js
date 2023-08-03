
    $(document).ready(function(){

      

      if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
        }
      
      var table_ip = $("#datatable").DataTable();
      valuedict = {};
      var i=1;

      $(".tableclass").fadeOut(0);    
      $("#exports").hide();

      
      


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




      $("#btn1").click(function(){



        var ip = document.getElementById('inputtext');
        var device = document.getElementById('device_type');
        var username= document.getElementById('username');
        var password= document.getElementById('password');
        const haskey = valuedict.hasOwnProperty(ip.value) 


        valuedict[ip.value] = {}
        

        if (ip.value != "" && haskey == false && device.val != "Default" ){
        valuedict[ip.value]['device_make'] = device.value;
        valuedict[ip.value]['username'] = username.value;
        valuedict[ip.value]['password'] = password.value;
        
      console.log(ip.value,'ip.value')
      
      if( regLast.test(ip.value)){
        console.log("yes")
      }

      else {
        console.log("nooooooo")
      }


      $(".tableclass").fadeIn();


      table_ip.row.add([i , ip.value ,  device.value,  username.value, "</td><td><select >"+"<option value='Inactive' hidden>Choose to Delete</option>"+"<option value='Active' >Delete</option>"+"</select>"]).draw(false);
      i+=1;
      ip.value = "";
      username.value="";
      password.value="";
      $('#device_type option').prop('selected', function(){
        return this.defaultSelected;
      })  


      $('#datatable').find('tr').change( function(data){
        var myrow = $(this).find('td:eq(1)').text();
        

        var removingRow = $(this).closest('tr');

        table_ip.row(removingRow).remove().draw();

        delete valuedict[myrow]
        console.log(valuedict,'=====after delete')
      });
          // alert("IP already exits/Input IP is Empty")
          // $("#ipError").html("Input IP is Empty !!").addClass("test-danger");
        
   
      }
      else {
        console.log("IP already exits/Input IP is Empty")

        
        


      }
      


      })
    

      $("#deleteAll").click(function() {
        $('#datatable').DataTable().clear().draw();
        valuedict = {};
     });


      $("#Ipsubmit").click(function(e){
        e.preventDefault();
        
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

              $('#Activity_name option').prop('selected', function(){
                return this.defaultSelected;
              })
              $("#exports").show();
            },
        })
      })




});
 

    
   
