@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div>
@if (!empty($messageToUser))
<h2 style="text-align:center"><span style="background-color:rgba(0,231,0,0.5);border:5px solid #000;border-radius:10px;padding:5px 10px 5px 10px">{{$messageToUser}}</span></h2>
@endif
            <div class="panel panel-default">
                <div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">View Booking Availability For Customer: {{$user->name}}</div>


<div class="panel-body">

                    @foreach ($employees as $employee)
<h4>Make A Booking With {{$employee->name}} For A {{$service->name}}</h4>

<table width="100%" style="border-collapse:collapse">
<tr>
                        @foreach (App\Providers\AppServiceProvider::getNextDays(0, 6) as $date)
<th style="border:1px solid #000; width:14.28%; text-align:center">{{App\Providers\AppServiceProvider::day_of_week_as_text($date['day_of_week'])}}
<br>
{{App\Providers\AppServiceProvider::month_as_short_text($date['month'])}} {{$date['day']}}
</th>
                        @endforeach
</tr>

<tr style="border-bottom:1px solid #000">
                        @foreach (App\Providers\AppServiceProvider::getNextDays(0, 6) as $date)
                            <?php $availableBookings = $employee->availableBookings($user, $service, $date['day_of_week']); ?>
                            @if (count($availableBookings))
<td style="border:1px solid #000; padding-top:0.2em; text-align:center; vertical-align:top">
                                @foreach ($availableBookings as $booking)
<p>
<a href="/make-new-booking/{{$booking['user']->id}}/{{$booking['service']->id}}/{{$booking['employee']->id}}/{{$booking['day_of_week']}}/{{$booking['start_time']}}">
{{$booking['start_time']}}-{{App\Providers\AppServiceProvider::add_minutes($booking['start_time'], $service->duration_in_minutes)}}
</a>
</p>
                                @endforeach
</td>
                            @else
<td style="border:1px solid #000; padding-top:0.2em; text-align:center; vertical-align:center">
<p>
N/A
</p>
</td>
                            @endif
                        @endforeach
</tr>
</table>
<hr>
                    @endforeach



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

