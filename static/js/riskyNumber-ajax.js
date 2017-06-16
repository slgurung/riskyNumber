$(document).ready(function() {
    $('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/riskyNumber/suggest/', {suggestion: query}, function(data){
            $('#stocks').html(data);
            });
    });
    $("#tickerForm").on("submit", function(e){
        e.preventDefault();  
        $.ajax({
            url: "/riskyNumber/quote/",
            type: "get",
            data: {
                ticker: $("#suggestion").val()        
            },
            dataType: 'json',
            success: function(data){
                if(data.result == 'exist'){
                 window.location.href="/riskyNumber/summary/" + data.ticker +"/";       
                }else{
                    $("#suggestion").val("");
                    document.getElementById("suggestion").placeholder = "Ticker isn't in my list. Try another."; 
                    //$("#id_username").focus(); 
                    $("#suggestion").on("keydown", function(){
                        document.getElementById("suggestion").placeholder = "Ticker Search";         
                    });
                }  
            }
        });
    });  
  
    $("#loginForm").on("submit", function(e){
        e.preventDefault();
        if ($("#id_login_username").val() == ""){
            $("#id_login_username").focus();      
        }else if ($("#id_login_password").val() == ""){
            $("#id_login_password").focus(); 
        }else{
            auth_login(); 
            $("#tickerForm").focus();  
        }
    });

    $("#signupModal").on("shown.bs.modal", function(){
        $("#id_first_name").focus();            
    });

    $("#loginModal").on("shown.bs.modal", function(){
        $("#id_login_username").focus();            
    });
             
    $("#loginModal").on("hide.bs.modal", function(){
        clearLoginForm();
        document.getElementById("id_login_username").placeholder = "Enter Username";              
    });

    $("#signupModal").on("hide.bs.modal", function(){
        clearSignupForm();               
    });

    $("#openLogin").click(function(){
        $("#signupModal").on("hidden.bs.modal", function () {
            $("#loginModal").modal();
            $("#signupModal").off("hidden.bs.modal");
             
        });        
    });

    $("#openSignUp").click(function(){
        $("#loginModal").on("hidden.bs.modal", function () {
            $("#signupModal").modal();
            // removes hidden event form loginModal to prevent recursive event
            $("#loginModal").off("hidden.bs.modal");
            //$("#id_first_name").focus();  
        });    
    });

    $("#id_username").change(function () {
        var username = $(this).val();
        $.ajax({
            url: "/riskyNumber/validate_username/",
            type: "POST",
            data: {
                'username': username        
            },
            dataType: 'json',
            success: function(data){
                if(data.is_taken){
                    alert(data.error_message);    
                    $("#id_username").val("");
                    $("#id_username").focus();     
                }  
            }
        });
    });
    $("#id_password").change(function(){
        var psswd = $("#id_password").val();
        if (/[^A-Za-z0-9@.+-_]+/.test(psswd) || psswd.length < 5){
            alert("Invalid password. 5-30 characters long. Alphabet, number, @, ., _, -, and + only.");  
            $("#id_password").val("");
            $("#id_password").focus();       
        }
                            
    });

    $("#id_password2").focus(function(){
        var psswd = $("#id_password").val();
        if (psswd == ""){
            alert("First, enter a valid password at Password Input-Box & re-enter to verify.");  
            $("#id_password").val("");
            $("#id_password").focus();        
        }
    });

    $("#id_password2").change(function(){
        if ($("#id_password").val() != $("#id_password2").val()){
            alert("Don't match the password. Re-enter again."); 
            $("#id_password2").val("");
            $("#id_password2").focus();      
        }
    });
    // works on class but not on id
    $(".news").click(function(){
        //console.log('hello');  
        $("#suggestion").focus();           
    });

});

function clearSignupForm(){
    document.getElementById("signupForm").reset();        
}

function clearLoginForm(){
    document.getElementById("loginForm").reset();        
}

function auth_login(){
    $.ajax({
        url: "/riskyNumber/authenticate_login/",
        type: "POST",
        data: {uname: $("#id_login_username").val(),
                  pword: $("#id_login_password").val()},
        dataType: 'json',
        success: function(data){
                $("#id_login_username").val(""); 
                $("#id_login_password").val("");  
                 
                if (data.result == "success")
                {
                    $('#loginModal').modal('toggle');//close modal
                    window.location.href = "/riskyNumber/";
                }else if(data.result == "declined"){
                    $("#id_login_username").focus();  
                    document.getElementById("id_login_username").placeholder = "Username & password combination doesn't match. Try again.";
                }else if(data.result == "disabled"){
                    $('#loginModal').modal('toggle');//close modal
                    alert("Your account is disabled. Please contact administrator.")
                                
                }else{
                    $('#loginModal').modal('toggle');//close modal
                    alert("Not using POST. Try again.");
                }
        }
    }); 
}

function lineChart(x, y, mn, mx) {   
    var chartWidth = document.getElementById("line").parentElement.clientWidth;  
    var d3 = Plotly.d3;
            //need to put #                                         
    var gd3 = d3.select("#line") 
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "300px",
                });
    var gd = gd3.node();
    var data1 = {
                    x: x,
                    y: y,
                    mode: 'lines',
                    type: 'scatter',
                    fill: 'tozeroy',
                    line: {color:'rgb(0,170,230)'},
                    name: 'Price',            
            };
    
    var trace = [data1];
    var layout = {
                    autosize: true,
                    margin:{l:0, t:5, r:45, b:30, pad:0},  
                    dragmode: "pan",
                    showlegend: false,
                    xaxis: {
                            range: [start, end],
                            ticks: "outside",
                            type: "date",
                            fixedrange: false, 
                            showgrid: false,
                            //autorange: false,
                            tickformat: "%I:%M %p",
                            //tickmode: "auto",
                            linecolor: "#fff",
                            tickfont: { size:10, color:'rgb(0, 120, 180)' },
                            },
                    yaxis: {
                            fixedrange: true,
                            range: [mn, mx],
                            side: "right",
                            separatethousands: true,
                            exponentformat: "none",
                            
                            },
                             
                };
    document.getElementById("scatter").innerHTML = symbol + ": " + name;
    Plotly.newPlot(gd, trace, layout, {scrollZoom: true, 
                                            displayModeBar: false });
                                       
} // end of lineChart() tickformat: "%I:%M %p,%b %d'%y",

function lineChartD5(x, y, mn, mx) {   
    var chartWidth = document.getElementById("line").parentElement.clientWidth;  
    var d3 = Plotly.d3;
            //need to put #                                         
    var gd3 = d3.select("#line") 
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "300px",
                });
    var gd = gd3.node();
<<<<<<< HEAD
    x = x.map(function(d){
                            var dList = d.toString().split(" ");
                            return dList[0] +" " + dList[2] +", " + dList[4]; 

                    });


=======
    
>>>>>>> 0c3af658d8db9741dd98d04d717d460cebccc4f7
    var data1 = {
                    x: x,
                    y: y,
                    mode: 'lines',
                    type: 'scatter',
                    fill: 'tozeroy',
                    line: {color:'rgb(0,170,230)'},
                    name: 'Price',            
            };
    
    var trace = [data1];
    var layout = {
                    autosize: true,
                    margin:{l:0, t:5, r:45, b:30, pad:0},  
                    dragmode: "pan",
                    showlegend: false,
                    xaxis: {
<<<<<<< HEAD
                            range: [start, end],
=======
                            //range: [start, end],
>>>>>>> 0c3af658d8db9741dd98d04d717d460cebccc4f7
                            ticks: "outside",
                            type: "category",
                            fixedrange: false, 
                            showgrid: false,
                            //autorange: false,
                            //tickformat: "%I:%M %p,%b %d'%y",
<<<<<<< HEAD
                            tickformat: "%I:%M %p",
=======
                            //tickformat: "%I:%M %p",
>>>>>>> 0c3af658d8db9741dd98d04d717d460cebccc4f7
                            nticks: 4,
                            //tickmode: "auto",
                            linecolor: "#fff",
                            tickfont: { size:10, color:'rgb(0, 120, 180)' },
                            },
                    yaxis: {
                            fixedrange: true,
                            range: [mn, mx],
                            side: "right",
                            separatethousands: true,
                            exponentformat: "none",
<<<<<<< HEAD
                            
=======
                            nticks: 5,
>>>>>>> 0c3af658d8db9741dd98d04d717d460cebccc4f7
                            },
                             
                };
    document.getElementById("scatter").innerHTML = symbol + ": " + name;
    Plotly.newPlot(gd, trace, layout, {scrollZoom: true, 
                                            displayModeBar: false });
                                       
} // end of lineChart()


function hLineChart(x, y, v, mn, mx) { 
    document.getElementById("scatter").innerHTML = symbol + ": " + name;
                                   
    var chartWidth = document.getElementById("line").parentElement.clientWidth;                       
    var d3 = Plotly.d3; 
    //need to put #                                         
    var gd3 = d3.select("#line") 
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "300px",
                });
    var gd = gd3.node(); //make global variable
            
    var data1 = {
                x: x,
                y: y,
                mode: 'lines',
                type: 'scatter',
                fill: 'tozeroy',
                line: {color:'rgb(0,200,255)'},
                name: 'Price',  
                    
            };
    var data2 = {
                x: x,
                y: v,
                yaxis: 'y2',
                //xaxis: 'x2',
                type: "bar",
                marker: {
                        color: 'rgb(0, 115, 150)'
                },  
                name: 'Volume',
                hoverinfo: "skip",
            };
    var trace = [data1, data2];
            
    var layout = {
                autosize: true, 
                margin:{l:0, t:5, r:45, b:30, pad:0},  
                dragmode: "pan",
                showlegend: false,
                xaxis: {
                        ticks: "outside",
                        type: "category",
                        fixedrange: false, 
                        showgrid: false,
                        nticks: 4,
                        linecolor: "#fff",
                        side: "bottom",
                        tickfont: {size:10, color:'rgb(0, 120, 180)'},
                    },                    
                yaxis: {
                        fixedrange: true,
                        range: [mn, mx],
                        side: "right",
                        separatethousands: true,
                        exponentformat: "none",
                        nticks: 5,
                        overlaying: "y2",
                            
                    },
                yaxis2: {
                        range: [volmn, volmx],
                        fixedrange: true,
                        //overlaying: "y",
                        showgrid: false,
                    },
                };
    Plotly.newPlot(gd, trace, layout, {scrollZoom: true, 
                                            displayModeBar: false });
                                     
} // end of hLineChart()

function hCandleChart(x, o, h, l, c, mn, mx) {  
            var chartWidth = document.getElementById("line").parentElement.clientWidth;    
            var d3 = Plotly.d3; 
            var gd3 = d3.select("#candle")
                        .style({
                                width: (chartWidth - 2) +'px' ,
                                height: "300px"
                           });
            var gd = gd3.node(); 
             
            //console.log(x.map(function(d) { return new Date(d); }));          
            var fig = PlotlyFinance.createCandlestick(
                    {
                        open: o, 
                        high: h,
                        low: l,
                        close: c,
                        dates: x.map(function(d) { return new Date(d); })
                        
                    }
                );
            
            fig.layout.autosize = true;
            fig.layout.margin = {l:0, t:5, r:45, b:30, pad:0};
            fig.layout.dragmode = "pan";
            
            fig.layout.xaxis = {
                            nticks: 4,
                            type: "date",
                            ticks: "outside",
                            //tickvals:x,
                            //ticktext:x,
                            fixedrange: false, 
                            //autorange: false,
                            showgrid: false,
                            linecolor: "#fff",
                            side: "bottom",
                            tickfont: {size:10, color:'rgb(0, 120, 180)' },
                            
                        };    
                    
            fig.layout.yaxis = {
                            range : [mn, mx],
                            fixedrange: false,
                            side: "right",
                            separatethousands: true,
                            nticks: 6,
                            
                        };
                    
            Plotly.newPlot(gd, fig.data, fig.layout, {scrollZoom: true, 
                                            displayModeBar: false });     
                                  
} // end of hCandleChart() 


function candleChart(x, o, h, l, c, mn, mx) { 
    var chartWidth = document.getElementById("line").parentElement.clientWidth;    
    var d3 = Plotly.d3; 
    var gd3 = d3.select("#candle")
                .style({
                        width: (chartWidth - 2) +'px' ,
                        height: "300px"
                });
    var gd = gd3.node(); 
    var fig = PlotlyFinance.createCandlestick(
                    {
                        open: o, 
                        high: h,
                        low: l,
                        close: c,
                        dates: x
                            //.map(function(d) { return new Date(d); })
                    }
            );
            
    fig.layout.autosize = true;
    fig.layout.margin = {l:0, t:5, r:45, b:30, pad:0};
    fig.layout.dragmode = "pan";
    fig.layout.xaxis = {
                            type: "date",
                            range: [start, end],
                            fixedrange: false, 
                            showgrid: false,
                            //autorange: false,
                            tickformat: "%I:%M %p",
                            linecolor: "#fff",
                            side: "bottom",
                            tickfont: {size:10, color:'rgb(0, 120, 180)' },
            };       
    fig.layout.yaxis = {
                            range : [mn, mx],
                            fixedrange: false,
                            side: "right",
                            separatethousands: true,
                            //tickmode: "auto",
            };
           
    Plotly.newPlot(gd, fig.data, fig.layout, {scrollZoom: true, 
                                            displayModeBar: false });     
                                  
} // end of candleChart() 

function resizeChart(w){
    var activeTab = $(".tab-content").find(".active");
    var id = activeTab.attr('id');
    var d3 = Plotly.d3; 
             
    var gd3;                      
               
    gd3 = d3.select("#" + id);
               
    var gd = gd3.node();   
    var update = {
                    width: w -2 
            };                
    Plotly.relayout(gd, update);    
}

$(document).ready(function(){
    $(".nav-tabs a").click(function(event){
        event.preventDefault(); 
        var id = $(this).attr("id"); //get id value
        if (chartType == id){
            //console.log('return early');
            return;
        }
        $(this).tab('show'); 
                
        //console.log('chartype ' + chartType, 'chartperiod ' + chartPeriod );
        if ( id == "candlestick"){
            chartType = "candlestick";
            if (chartPeriod == 'd1'){
                candleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);  
            }else {
                hCandleChart(dateVal, openVal, highVal, lowVal, closeVal, min, max);  
            }
        }else if (id == "scatter"){
            chartType = "scatter";    
            if(chartPeriod == 'd1'){
                lineChart(dateVal, closeVal, min, max); 
            }else if(chartPeriod == 'd5'){
                lineChartD5(dateVal, closeVal, min, max); 
            }else{
                hLineChart(dateVal, closeVal, vol, min, max);       
            }
        }else{
            chartType = "fillingList";    
            
            $.ajax({
                    url: "/riskyNumber/fillings/",
                    type: "POST",
                    data: {
                        'ticker': window.symbol,        
                    },
                    dataType: 'json',
                    success: function(data){
                                    if (data.result == "gotIt"){
                                        var fillingNum = data.form.length;
                                        var list ="<strong style='color:rgb(0, 172, 230);'>&nbsp &nbsp Recent ";
                                        list += fillingNum + " fillings:</strong><ul>";
                                        for( i=0; i < fillingNum; i++){
                                            list += "<li><a class='fillingSource' href=" + data.dUrl[i] + " target=_blank>" + data.form[i] 
                                                + ", (" + data.fDate[i] + "): " + data.des[i] + "</a></li>";
                                                
                                        }
                                        list += "</ul>";
                                    }else if(data.result == "invalid"){
                                        var list = "<br>&nbsp &nbsp There are no fillings for stock index.";        
                                    }
                                    $("#filling").html(list);
                                    $(".fillingSource").click(function(){
                                        $("#suggestion").focus();           
                                    }); 
                            }
            });
        }
    }); 
    $(".histChart a").click(function(e){
        e.preventDefault(); 
        var id = $(this).attr("id");
       
        if (chartPeriod != id)
        {
            chartPeriod = id;
            //console.log(id + symbol);
            $.ajax({
                    url: "/riskyNumber/hChart/",
                    type: "POST",
                    data: {"chartPeriod": id, "ticker": symbol},
                    dataType: "json",
                    success: function(data){
                                $("#scatter").tab('show');
                                chartType = "scatter";   
                                dateVal = data.dateVal;   
                                vol = data.vol;
                                min = data.min;
                                max = data.max;
                                openVal = data.open; 
                                highVal = data.high;
                                lowVal = data.low;
                                closeVal = data.close;   
                                volmn = data.volMin;
                                volmx = data.volMax;
                                //console.log(dateVal); 
                                if ((chartPeriod != 'd1') && (chartPeriod != 'd5')){  
                                    hLineChart(dateVal, closeVal, vol, min, max);  
<<<<<<< HEAD
                                }else{
                                    dateVal = dateVal.map(function(d) {return new Date(d * 1000);});
                                    start = data.start;
                                    end = data.end;
                                    if (chartPeriod == 'd5'){
                                        
                                        lineChartD5(dateVal, closeVal, min, max); 

                                    }else {
                                        lineChart(dateVal, closeVal, min, max); 
                                    }
                                            
=======
                                }else if (chartPeriod == 'd5'){
                                    lineChartD5(dateVal, closeVal, min, max); 
                                }else {
                                    //dateVal = dateVal.map(function(d) {return new Date(d * 1000);});
                                    start = data.start;
                                    end = data.end;
                                    lineChart(dateVal, closeVal, min, max); 
>>>>>>> 0c3af658d8db9741dd98d04d717d460cebccc4f7
                                }
                            },
                    
             });
        }
        
    });
     
    $(window).resize(function(){
        //updates chartWidth
        var chartWidth = document.getElementById("line").parentElement.clientWidth;                  
        resizeChart(chartWidth);
    });
            
    lineChart(dateVal, closeVal, min, max);
});  
                                        
                                        
$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});        
   
     
        
