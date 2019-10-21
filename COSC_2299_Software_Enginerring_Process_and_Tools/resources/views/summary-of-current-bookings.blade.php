@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div>
@if (!empty($messageToUser))
<h2 style="text-align:center"><span style="background-color:rgba(0,231,0,0.5);border:5px solid #000;border-radius:10px;padding:5px 10px 5px 10px">{{$messageToUser}}</span></h2>
@endif
            <div class="panel panel-default">
                <div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">Summary Of Current Bookings</div>


<div class="panel-body">
<table width="100%" style="border-collapse:collapse">
<tr style="border-bottom:1px solid #000">
<th >Day</th>
<th >Time</th>
<th >Employee</th>
<th >Service</th>
<th>Customer</th>
</tr>


                        @foreach ($bookings as $booking)
<tr style="border-bottom:1px solid #000">
<td width="16.6%" style="padding-top:0.2em">
{{App\Providers\AppServiceProvider::day_of_week_as_text($booking->day_of_week)}}
{{App\Providers\AppServiceProvider::month_as_text($booking->month())}}
{{$booking->day()}}
</td>
<td width="16.6%" style="padding-top:0.2em">
{{$booking->start_time}}-{{App\Providers\AppServiceProvider::add_minutes($booking->start_time, $booking->service->duration_in_minutes)}}
</td>
<td width="16.6%" style="padding-top:0.2em">
{{$booking->employee->name}}
</td>
<td width="16.6%" style="padding-top:0.2em">
{{$booking->service->name}}
</td>
<td width="16.6%" style="padding-top:0.2em">
{{$booking->user->name}}
</td>
</tr>
                        @endforeach




</table>
<br>
<p style="font-weight:bold">Number of Bookings: {{count($bookings)}}</p>

<p>
<br>
<a href="/home">Home</a>
</p>

</div>


</div>
</div>
</div>
</div>
</div>

@stop

