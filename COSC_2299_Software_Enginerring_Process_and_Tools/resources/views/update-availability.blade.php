@extends('layouts.app')

@section('content')

<div class="container">
    <div class="row">
        <div>
            <div class="panel panel-default">
                <div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">Update Availability</div>


    <div class="panel-body">

<table width="100%" style="border-collapse:collapse">
<tr style="border-bottom:1px solid #000">
<th>Employee</th>
@for ($i=1; $i<=7; $i++)
<th style="text-align:center">{{App\Providers\AppServiceProvider::day_of_week_as_text($i)}}</th>
@endfor
</tr>
<tr style="border-bottom:1px solid #000">
<td width="30%" style="padding-top:0.2em">
{{ $employee->name }}<br>
{{$employee->address}}<br>
{{$employee->city}}
{{$employee->state}}
{{$employee->postcode}}
<br>
Phone: {{$employee->phone}}<br>
Email: <a href="mailto:{{$employee->email}}">{{$employee->email}}</a>
</td>

                    @for ($i=1; $i<=7; $i++)
                        @if ($i == $availability->day_of_week)
<td width="10%" style="text-align:center;background-color:rgba(255,255,0,0.5)">
                        @else
<td width="10%" style="text-align:center">
                        @endif
<a href="/update-availability/{{$employee->id}}/{{$i}}">
                        @if ($employee->availability($i))
{{$employee->availability($i)->start_time}}-{{$employee->availability($i)->end_time}}
                        @else
None
                        @endif
</a>
</td>
                    @endfor
</tr>
</table>
</div>

<div class="panel-body">

        <form action="/update-availability" method="POST" class="form-horizontal">
            {{ csrf_field() }}

<input type=hidden name="employee_id" value="{{$availability->employee_id}}">
<input type=hidden name="day_of_week" value="{{$availability->day_of_week}}">
            <div class="form-group{{ $errors->has('start_time') ? ' has-error' : '' }}">
                <label for="task" class="col-sm-3 control-label">Start Time</label>

                <div class="col-sm-2">
                    <input type="text" name="start_time" id="start_time" class="form-control" value="{{$availability->start_time}}" placeholder="Example: 900">
                                @if ($errors->has('start_time'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('start_time') }}</strong>
                                    </span>
                                @endif
                </div>
            </div>
            <div class="form-group{{ $errors->has('end_time') ? ' has-error' : '' }}">
                <label for="task" class="col-sm-3 control-label">End Time</label>

                <div class="col-sm-2">
                    <input type="text" name="end_time" id="end_time" class="form-control" value="{{$availability->end_time}}" placeholder="Example: 1700">
                                @if ($errors->has('end_time'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('end_time') }}</strong>
                                    </span>
                                @endif
                </div>
            </div>

            <div class="form-group">
                <div class="col-sm-offset-3 col-sm-6">
<ul>
<li>Times are entered in 24 hour format</li>
<li>Use numbers only</li>
<li>Must be a number between 0 and 2359</li>
<li>For example, 900 is 9:00am and 1700 is 5:00pm</li>
</ul>
                </div>
            </div>

            <div class="form-group">
                <div class="col-sm-offset-3 col-sm-6">
                    <button type="submit" class="btn btn-default">
                        <i class="fa fa-plus"></i> Update Availability
                    </button>
                    or <a href="/delete-availability/{{$availability->employee_id}}/{{$availability->day_of_week}}">clear availability</a>
                </div>
            </div>

            <div class="form-group">
                <div class="col-sm-offset-3 col-sm-6">
<a href="/show-availabilities-for-each-employee">Show Availabilities For Each Employee</a>
                </div>
            </div>
        </form>


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

