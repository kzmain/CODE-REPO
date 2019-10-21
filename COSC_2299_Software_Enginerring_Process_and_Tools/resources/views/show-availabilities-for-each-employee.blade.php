@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div>
            <div class="panel panel-default">
                <div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">Availabilities of Employees</div>


<div class="panel-body">
<table width="100%" style="border-collapse:collapse">
<tr style="border-bottom:1px solid #000">
<th>Employee</th>
@for ($i=1; $i<=7; $i++)
<th style="text-align:center">{{App\Providers\AppServiceProvider::day_of_week_as_text($i)}}</th>
@endfor
</tr>
                        @foreach ($employees as $employee)
<tr style="border-bottom:1px solid #000">
<td width="30%" style="padding-top:0.2em">
{{$employee->name}}<br>
{{$employee->address}}<br>
{{$employee->city}}
{{$employee->state}}
{{$employee->postcode}}<br>
Phone: {{$employee->phone}}<br>
Email: <a href="{{$employee->email}}">{{$employee->email}}</a>
</td>

                    @for ($i=1; $i<=7; $i++)
<td width="10%" style="text-align:center">
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
                        @endforeach
</table>
<br>
<p style="font-weight:bold">Number of Employees: {{count($employees)}}</p>

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

