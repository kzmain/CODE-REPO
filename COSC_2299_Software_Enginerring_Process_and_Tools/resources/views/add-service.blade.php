@extends('layouts.app')

@section('content')

<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">
@if (!empty($messageToUser))
<h2 style="text-align:center"><span style="background-color:rgba(0,231,0,0.5);border:5px solid #000;border-radius:10px;padding:5px 10px 5px 10px">{{$messageToUser}}</span></h2>
@endif
            <div class="panel panel-default">
                <div class="panel-heading" style="background-color:#636bcf; font-size:1.7em; color:yellow; text-shadow: 0px 1px #000000;">Add Service</div>



    <div class="panel-body">

<table width="100%" style="border-collapse:collapse">
<tr style="border-bottom:1px solid #000">
<th>Service</th>
<th>Duration In Minutes</th>
</tr>

                        @foreach ($services as $service)
<tr style="border-bottom:1px solid #000">
<td style="padding-top:0.2em">
{{ $service->name }}
</td>
<td style="padding-top:0.2em">
{{$service->duration_in_minutes}}
</td>
</tr>
                        @endforeach


</table>
<br>
<p style="font-weight:bold">Number of Services: {{count($services)}}</p>

</div>


    <div class="panel-body">

        <form action="/handle-add-service" method="POST" class="form-horizontal">
            {{ csrf_field() }}

            <div class="form-group{{ $errors->has('name') ? ' has-error' : '' }}">
                <label for="task" class="col-sm-3 control-label">New Service</label>

                <div class="col-sm-6">
                    <input type="text" name="name" id="name" class="form-control" value="{{ old('name') }}" placeholder="Enter name for new service...">
                                @if ($errors->has('name'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('name') }}</strong>
                                    </span>
                                @endif
                </div>
            </div>

            <div class="form-group{{ $errors->has('duration_in_minutes') ? ' has-error' : '' }}">
                <label for="task" class="col-sm-3 control-label">Duration In Minutes</label>

                <div class="col-sm-6">
                    <input type="text" name="duration_in_minutes" id="duration_in_minutes" class="form-control" value="{{ old('duration_in_minutes') }}" placeholder="Enter duration in minutes...">
                                @if ($errors->has('duration_in_minutes'))
                                    <span class="help-block">
                                        <strong>{{ $errors->first('duration_in_minutes') }}</strong>
                                    </span>
                                @endif
                </div>
            </div>

            <div class="form-group">
                <div class="col-sm-offset-3 col-sm-6">
                    <button type="submit" class="btn btn-default">
                        <i class="fa fa-plus"></i> Add Service
                    </button>
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

