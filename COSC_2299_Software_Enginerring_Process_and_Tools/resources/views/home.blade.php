@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
@if (!empty($messageToUser))
<h2 style="text-align:center"><span style="background-color:rgba(0,231,0,0.5);border:5px solid #000;border-radius:10px;padding:5px 10px 5px 10px">{{$messageToUser}}</span></h2>
@endif
            <div class="panel panel-default">

<div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">
@if ($user->business)
Admin Menu
@else
Customer Menu
@endif
</div>

                <div class="panel-body">
@if ($user->business)
<p>
<ul>
<li><a href="/add-employee">Add Employee</a></li>
<li><a href="/show-availabilities-for-each-employee">Availabilities of Employees</a></li>
<li><a href="/summary-of-past-bookings">Summary of Past Bookings</a></li>
<li><a href="/summary-of-current-bookings">Summary of Current Bookings</a></li>
<li><a href="/admin-new-booking">New Booking</a></li>
<li><a href="/add-service">Add Service</a></li>
</ul>
</p>
@else

<h3>View Availability For Service:</h3>
<br>
@foreach ($services as $service)
<div style="float:left; background-color:#02; border-style: double; margin:auto; padding:10px"><a href="/view-booking-availability/{{$user->id}}/{{$service->id}}">{{$service->name}}</a></div>

@endforeach
<p style="clear:both">
<br>
OR
		@include('bookingPannel.bookingFilterPannel')
<p style="clear:both">
<br>
@endif


        @if ($user->email == env('DEBUG_USER_EMAIL', 'debug@example.com'))
<hr>
For Debugging
<ul>
<li><a href="/debug/user">Users</a></li>
<li><a href="/debug/booking">Bookings</a></li>
<li><a href="/debug/availability">Availabilities</a></li>
<li><a href="/debug/employee">Employees</a></li>
<li><a href="/debug/service">Services</a></li>
<li><a href="/debug/business">Businesses</a></li>
<li><a href="/debug/choose-view-available">New Booking</a></li>
</ul>
        @endif
</p>

                </div>
            </div>
        </div>
    </div>
</div>
@endsection
