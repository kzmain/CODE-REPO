@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
@if (!empty($messageToUser))
<h2 style="text-align:center"><span style="background-color:rgba(0,231,0,0.5);border:5px solid #000;border-radius:10px;padding:5px 10px 5px 10px">{{$messageToUser}}</span></h2>
@endif
            <div class="panel panel-default">
                <div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">Booking Confirmation</div>


                <div class="panel-body">

<table>
<tr>
<th style="padding-left:3em;text-align:right">Customer:</td>
<td style="padding-left:1em;vertical-align:top">{{$booking->user->name}}</td>
</tr>
<tr>
<th style="padding-left:3em;text-align:right">Service:</td>
<td style="padding-left:1em;vertical-align:top">{{$booking->service->name}}</td>
</tr>
<tr>
<th style="padding-left:3em;text-align:right">Employee:</td>
<td style="padding-left:1em;vertical-align:top">{{$booking->employee->name}}</td>
</tr>
<tr>
<th style="padding-left:3em;text-align:right">Day:</td>
<td style="padding-left:1em;vertical-align:top">
{{App\Providers\AppServiceProvider::day_of_week_as_text($booking->day_of_week)}}
{{App\Providers\AppServiceProvider::month_as_text($booking->month())}}
{{$booking->day()}}
</td>
</tr>
<tr>
<th style="text-align:right">Time:</td>
<td style="padding-left:1em;vertical-align:top">
{{$booking->start_time}}-{{App\Providers\AppServiceProvider::add_minutes($booking->start_time, $booking->service->duration_in_minutes)}}
</td>
</tr>
</table>

<p>
<br>
<a href="/home">Home</a>
</p>

                </div>
            </div>
        </div>
    </div>
</div>
@endsection
