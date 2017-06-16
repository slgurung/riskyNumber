<!DOCTYPE html> 
{% load staticfiles %} 


<html lang="en"> 
<head>
    <title> 
        {% block title_block %}
            Equity Trade!
        {% endblock %} 
    </title> 
    <meta charset="utf-8"> 
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    
    <link rel="icon" href="{% static "images/favicon.ico" %}" /> 
    <link rel="stylesheet" href="{% static "js/signin.css" %}" /> 
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
    <script src="https://d3js.org/d3.v4.min.js"></script> 
    
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdn.rawgit.com/etpinard/plotlyjs-finance/master/plotlyjs-finance.js"></script>
    
    <style>
        body {
            padding:10px 5px 10px 5px;
        }
        div#contentDiv {
            position:relative;
            padding:5px 15px 0px 15px;
            
        }
        
        .modal-header, h4, .close {
              background-color: #5cb85c;
              color:white !important;
              text-align: center;
              font-size: 30px;
          }
        
        .modal-footer {
              background-color: #f9f9f9;
          }
       
         
    </style>
</head> 
<body>  
    
    <nav class="navbar navbar-default" style="background-color:rgb(0,150,190);border-color:white;margin-bottom:0px;"> 
    <div class="container" style="max-width:1000px;">     
        <div class="navbar-header" >
            <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#topNavbar" style="border-color:white;">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#" style="color:rgb(0,51,51);" >riskyNumber</a> 
        </div>
        <div class="collapse navbar-collapse" id="topNavbar" > 
            <ul class="nav navbar-nav"> 
                <li><a class="nav-item nav-link" href="{% url 'home' %}" style="color:rgb(0, 60, 77);font-size: 16px;">
                                                       <span class="glyphicon glyphicon-home"></span></a></li>
                <li><a class="nav-item nav-link" href="{% url 'summary' '.INX' %}" style="color:	white">S&P 500</a></li>
                <li><a class="nav-item nav-link" href="{% url 'summary' '.DJI' %}" style="color:white;">DJI</a></li>  
                <li><a class="nav-item nav-link" href="{% url 'summary' '.IXIC' %}" style="color:white;">Nasdaq</a></li>                     
                <!-- put search here later 
                -->
            </ul>
            {% if user.is_authenticated %}
            <ul class="nav navbar-nav navbar-right" >
                <li><a class="nav-item nav-link" style="color:rgb(0, 60, 77);"
                    href="{% url 'auth_logout' %}?next=/riskyNumber/">Logout</a> </li>
                 <li><a class="nav-item nav-link" style="color:rgb(0, 60, 77);"
                    href="#">Profile</a></li>
                
            </ul>
            {% else %} 
            <ul class="nav navbar-nav navbar-right">
                <!-- <li><a href="{% url 'registration_register' %}"> -->
                <li><a data-toggle="modal" href="#signupModal" style="color:rgb(0, 60, 77);">
                    <span class="glyphicon glyphicon-user"></span> Sign Up</a></li>
                <!--<li><a href="{% url 'auth_login' %}"> -->
                <li><a data-toggle="modal"  href="#loginModal" style="color:rgb(0, 60, 77);"> 
                    <span class="glyphicon glyphicon-log-in"></span> Login</a></li>
            </ul>
            {% endif %} 
        </div>
    </div> 
    </nav> 
    
    <!-- login modal starts -->
    
    <div class="container">
    
    <!-- Modal -->
    <div class="modal fade" id="loginModal" role="dialog">
        <div class="modal-dialog">
    
      <!-- Modal content-->
            <div class="modal-content">
                <div class="modal-header" style="padding:35px 50px;background-color:rgb(0, 163, 204);">
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                    <h4 style="background-color:rgb(0, 163, 204);"><span class="glyphicon glyphicon-lock"></span> Login</h4>
                </div>
                <div class="modal-body" style="padding:40px 50px;">
                    <div id="user_login">
                        <form id="loginForm" method="post">
                            {% csrf_token %} 
                            <div class="form-group">
                                <label for="id_login_username"><span class="glyphicon glyphicon-user"></span> Username</label>
                                <input type="text" class="form-control" id="id_login_username" name="login_username" placeholder="Enter Username">
                            </div>
                            <div class="form-group">
                                <label for="id_login_password"><span class="glyphicon glyphicon-eye-open"></span> Password</label>
                                <input type="password" class="form-control" id="id_login_password" name="login_password" placeholder="Enter password">
                            </div>
                            <div class="checkbox">
                                <label><input type="checkbox" value="" checked>Remember me</label>
                            </div>
                            <button type="submit" id="loginBtn" class="btn btn-success btn-block" style="background-color:rgb(0, 163, 204);">
                            <span class="glyphicon glyphicon-off"></span> Login</button>
                        </form>  
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary pull-left" onclick="clearLoginForm()"
                                style="background-color:rgb(0, 163, 204); width:80px;">Reset</button>
                    <label>Not a member? <button id="openSignUp" type="button" class="btn btn-info" 
                                                      data-dismiss="modal">Sign Up</button></label>
                    <p>Forgot <a href="#">Password?</a></p>
                </div>
            </div>
          </div> 
    </div>
    </div>
       
    <!-- sign-in modal end -->
          
    <!---- signup modal starts -->
    
    <div class="container">
    <!-- Modal -->
        <div class="modal fade" id="signupModal" role="dialog">
            <div class="modal-dialog">
    
            <!-- Modal content-->
                <div class="modal-content">
                    <div class="modal-header" style="padding:35px 50px;background-color:rgb(0, 163, 204);">
                        <button type="button" class="close" data-dismiss="modal" >&times;</button>
                        <h4 style="background-color:rgb(0, 163, 204);">
                            <span  class="glyphicon glyphicon-lock"></span>Sign Up</h4>
                    </div>
                    <div class="modal-body" style="padding:40px 50px;">
                        <div id="user_registration">
                            <form class="form-horizontal" id="signupForm" method="post" action="{% url 'register' %}" 
                                enctype="multipart/form-data"> 
                                {% csrf_token %}
                                <div class="form-group">
                                    <label class="control-label col-md-3" for="id_first_name">First Name:</label>
                                    <div class="col-md-9">
                                        <input class="form-control" id="id_first_name" name="first_name"
                                            type="text" placeholder="Enter First Name"/>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label class="control-label col-md-3" for="id_last_name">Last Name:</label>
                                    <div class="col-md-9">
                                        <input class="form-control" id="id_last_name" name="last_name"
                                            type="text" placeholder="Enter Last Name"/>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label class="control-label col-md-3" for="id_username">Username:</label>
                                    <div class="col-md-9">
                                        <input class="form-control" id="id_username" maxlength="30"
                                            name="username" type="text" placeholder="Enter Username" required="">
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label class="control-label col-md-3" for="id_password">Password:</label>
                                    <div class="col-md-9">
                                        <input class="form-control" id="id_password" name="password"
                                            type="password" placeholder="Enter password" required/>
                                        <span class="helptext">
                                            30 characters or less. Alphanumeric, @, ., +, -, and _ only.
                                        </span>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label class="control-label col-md-3" for="id_password2">
                                            Re-enter:</label>
                                    <div class="col-md-9">
                                        <input class="form-control" id="id_password2" name="password2" placeholder="Re-enter password"
                                           type="password" required/>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label class="control-label col-md-3" for="id_email">
                                            E-mail:</label>
                                    <div class="col-md-9">
                                        <input class="form-control" id="id_email" name="email" type="email" 
                                            placeholder="Enter valid email" />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="col-sm-offset-3 col-md-9">
                                        <button type="submit" id="signupBtn" class="btn btn-primary" 
                                            style="background-color:rgb(0, 163, 204); width:80px;">Submit</button>
                                        
                                    </div>
                                </div>
                            </form> 
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary pull-left" onclick="clearSignupForm()"
                                              style="background-color:rgb(0, 163, 204); width:80px;">Reset</button>
                        <label>A member? <button id="openLogin" type="button" class="btn btn-info" 
                                                      data-dismiss="modal">Login</button></label>
                                    
                      <!--
                      <p>Forgot <a href="#">Password?</a></p>
                      -->
                    </div>
                </div>
            </div>
        </div> 
    </div>
    
    <!-- singup modal end -->
      
    <div class="container" style="max-width:1000px;"> 
        <div class="row"> 
            <div class="col-md-12">
                <table style="border-collapse: collapse;min-width:720px;">
                    <tr style="text-align:left;vertical-align:bottom;">
                        <th style="font-size:18px;"><span class="label label-success" style="color:rgb(168,31,31);">
                            Trending: </span></th>            
                        {% for t in trending %}
                            {% if forloop.last %}
                                <th ><a id= "{{t}}"  href="{% url 'summary' t %}">{{t}}</a></th>
                            {% else %}
                                <th ><a id= "{{t}}"  href="{% url 'summary' t %}">{{t}}-</a></th>
                            {% endif %}
                        {% endfor %}
                    </tr>
                </table>
            </div>
        </div>
        <hr style="margin:5px 0px 0px 0px;" />
    </div>
    
    <div class="container" id="contentDiv" style="max-width:1000px;">
        <div class="row">
            <div class="col-md-4">
                
                <form id = "tickerForm" method="get">
                    
                    <div class="input-group">
                        <div class="input-group-addon">
                            <span class="glyphicon glyphicon-search"></span>
                        </div>
                        <input class="search-query form-control" type="text" 
                            placeholder="Ticker Search" name="suggestion" value="" 
                            id="suggestion" autofocus/>
                    </div>
                </form>
                <div id="stocks">
                    {% if stocks %}
                        {% include 'riskyNumber/ticker.html' with stocks=stock_list %}
                    {% endif %}
                </div>
            
            </div>
            <div class="col-md-8">
            </div>
        </div>
    </div>
    
    <div class="container" id="contentDiv" style="max-width:1000px;">
        <div class="row" style="margin:0px 0px 0px 0px;" >
           <div class="col-md-12" style="border-color:rgb(0,150,190);border-style:solid;border-width:1px;
                    margin:5px 0px 0px 0px; padding:0px 0px 0px 0px;border-radius:10px 10px 10px 10px;  
                    background-color:rgb(242, 242, 242);">
                   
                {% block chart_block %}
                {% endblock %}
           </div> 
        </div>
    </div> 
    <div class="container" id="contentDiv" style="max-width:1000px;">
        <div class="row">
            <div class="col-md-12">
                {% block summary_block %}
                {% endblock %}
            </div>
        </div>
    </div>
    <div class="container" id="contentDiv" style="max-width:1000px;">
        <div class="row">
            <div class="col-md-6" id="stock_news">
                {% block stock_news %}
                {% endblock %}
            </div>
            <div class="col-md-6" id="business_news">
                {% block business_news %}
                {% endblock %}    
            </div>
        </div>
        <hr>
    </div>    
    <footer class="container-fluid text-center" style="max-width:1000px;">
        <div class="jumbotron" style="padding:10px 50px 10px 50px; margin:auto;">
            <div>
            <ul class="list-inline">
                <li><a href="{% url 'about' %}"><kbd>About riskyNumber</kbd></a></li>
            </ul>
            </div>
            <div>
                <p style="font-size:9px;"><span class="glyphicon glyphicon-copyright-mark"></span>Copyright 2017</p>
            </div>
            
        </div>
    </footer>
        <!-- Bootstrap core JavaScript ================================================== --> 
        <!-- Placed at the end of the document so the pages load faster --> 
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>    
    <script src="{% static "js/riskyNumber-ajax.js" %}"></script>      
   
          
</body>
</html>


                

