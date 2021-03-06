 //load data
 $(document).ready(function () {
    $.ajax({
        url: '/api/get_user_data',
        method: 'get',
        dataType: 'json',
        success: function (aData) {
            $('#name').html(aData.name);
            $('#uname').val(aData.name);
            $('#ustudentId').val(aData.studentId);
            $('#uphonenumber').val(aData.phone_number);
            $('#uemail').val(aData.email);
            $('#umoney').html(aData.money);
            let sHtml = `
            <table class="table table-bordered">
                <thead class="table-info">
                    <tr>
                        <th>Semester</th>
                        <th>Date of payment</th>
                        <th>Amount</th>
                        <th>Payer</th>
                    </tr>
                </thead>
                <tbody>`;
            aData.history.forEach(function (obj) {
                var total = obj.semester_tuition - obj.reduction;
                sHtml += `
                    <tr>
                        <td class="note">`+ obj.semester +`</td>
                        <td class="number">`+ obj.date_of_payment +`</td>
                        <td class="number">`+ total +`</td>
                        <td class="note">`+ obj.submitter_id + ` - ` + obj.name + `</td>
                    </tr>
                `;
            });
            sHtml += `</tbody></table>`;
            $('#a').html(sHtml);
        },
        beforeSend: function () {
            $('#loading').css('display', 'block');
        },
        complete: function () {
            $('#loading').css('display', 'none');
        }
    });
});

//search by student id
$('#fStudentId').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);

    $.ajax({
        url: '/api/get_semester',
        method: 'post',
        data: form.serialize(),
        dataType: 'json',
        success: function (aData) {
            $('#tuition').empty();
            if (aData.error != null) {
                alert(aData.error);
                $('#semesters').empty();
                $('#info-receiver').empty();
            } else {
                let sHtml = `
                    <label><b>Semester</b></label><br>
                    <select id="semester" class="form-control">
                        <option value="Choose semester">Choose semester</option>
                `;

                for (i in aData.semesters) {
                    sHtml += `<option value="` + aData.semesters[i] + `">` + aData.semesters[i] + `</option>`;
                }
                sHtml += `</select>`;
                $('#semesters').html(sHtml);

                sHtml = `
                <div class="row">
                    <div class="col-sm-4">
                        <label><b>Name</b></label>
                        <input type="text" class="form-control" id="rname" value="`+ aData.info[0].name + `" disabled>
                    </div>
                    <div class="col-sm-3">
                        <label><b>Phone number</b></label>
                        <input type="text" class="form-control" id="rphonenumber" value="`+ aData.info[0].phone_number + `" disabled>
                    </div>
                    <div class="col-sm-5">
                        <label><b>Email</b></label>
                        <input type="text" class="form-control" id="remail" value="`+ aData.info[0].email + `" disabled>
                    </div>
                </div>
                <hr>
                `;
                $('#info-receiver').html(sHtml);

                //change semester in dropbox and show tuition
                $('#semester').change(function () {
                    if ($(this).val() != 'Choose semester') {
                        $.ajax({
                            url: '/api/get_tuition',
                            method: 'post',
                            data: {
                                studentId: $('#studentId').val(),
                                semester: $(this).val()
                            },
                            dataType: 'json',
                            success: function (aDataTuition) {
                                if (aDataTuition.error != null) {
                                    alert(aDataTuition.error);
                                    $('#tuition').empty();
                                    $('#info-receiver').empty();
                                } else {
                                    sHtml = `<table class="table table-bordered">`;
                                    var total = aDataTuition.tuition[0].semester_tuition - aDataTuition.tuition[0].reduction;
                                    sHtml += `
                                        <thead class="table-info">
                                            <tr>
                                                <th>Semester Tuition</th>
                                                <th>Reduction</th>
                                                <th>Total tuition unpaid</th>
                                                <th>Note</th>
                                            </tr>
                                            <tr>
                                                <th>(1)</th>
                                                <th>(2)</th>
                                                <th>(3) = (1) - (2)</th>
                                                <th>(4)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td class="number">`+ aDataTuition.tuition[0].semester_tuition + `</td>
                                                <td class="number" id="total-tuition">`+ aDataTuition.tuition[0].reduction + `</td>
                                                <td class="number">`+ total + `</td>
                                                <td class="note">`+ aDataTuition.tuition[0].note + `</td>
                                            </tr>
                                        </tbody>
                                    `;
                                    sHtml += `</table>`;

                                    if (aDataTuition.tuition[0].note != 'COMPLETED') {
                                        sHtml += `
                                        <button type="button" class="btn btn-danger" data-toggle="modal" 
                                        data-target="#paymodal" id="pay">PAY</button>
                                        `;
                                        $('#tuition').html(sHtml);

                                        $('#pay').click(function () {
                                            sHtml = `
                                            <h6>Payer information</h6>
                                            <hr>
                                            <div class="row confirm">
                                                <div class="col-sm-5">
                                                    Student ID
                                                </div>
                                                <div class="col-sm-7">
                                                    <b>`+ $('#ustudentId').val() + `</b>
                                                </div>
                                            </div>
                                            <div class="row confirm">
                                                <div class="col-sm-5">
                                                    Name
                                                </div>
                                                <div class="col-sm-7">
                                                    <b>`+ $('#uname').val() + `</b>
                                                </div>
                                            </div>
                                            <hr>
                                            <h6>Receiver information</h6>
                                            <hr>
                                            <div class="row confirm">
                                                <div class="col-sm-5">Student ID</div>
                                                <div class="col-sm-7">
                                                    <b>`+ $('#studentId').val() + `</b>
                                                </div>
                                            </div>
                                            <div class="row confirm">
                                                <div class="col-sm-5">Name</div>
                                                <div class="col-sm-7">
                                                    <b>`+ $('#rname').val() + `</b>
                                                </div>
                                            </div>
                                            <hr>
                                            <div class="row confirm">
                                                <div class="col-sm-5">Semester</div>
                                                <div class="col-sm-7">
                                                    <b>`+ $('#semester').val() + `</b>
                                                </div>
                                            </div>
                                            <div class="row confirm">
                                                <div class="col-sm-5">Total tuition</div>
                                                <div class="col-sm-7">
                                                    <b>`+ total + `</b>
                                                </div>
                                            </div><br>
                                            <div class="row">
                                                <div class="col-sm-4">Enter OTP</div>
                                                <div class="col-sm-5">
                                                    <input class="form-control" name="otp" id="otp" type="number" pattern="/^-?\d+\.?\d*$/" 
                                                    onKeyPress="if (this.value.length == 6) return false;" 
                                                    onkeydown="javascript: return event.keyCode === 8 ||
                                                    event.keyCode === 46 ? true : !isNaN(Number(event.key))" />
                                                </div>
                                                <div class="col-sm-3" style="text-align: right;"><button type="button"
                                                    class="btn btn-warning" id="get-otp">Get OTP</button></div>
                                            </div>
                                            <hr>
                                            <div class="form-group"><button class="btn btn-primary btn-lg btn-block" 
                                                type="submit" id="payment">Pay</button></div>
                                            `;
                                            $('#body-confirm').html(sHtml);

                                            $('#get-otp').click(function () {
                                                $.ajax({
                                                    url: '/api/get_otp',
                                                    method: 'post',
                                                    dataType: 'text',
                                                    success: function (sData) {
                                                        alert(sData);
                                                    },
                                                    error: function () {
                                                        console.log('error');
                                                    },
                                                    beforeSend: function () {
                                                        $('#loading').css('display', 'block');
                                                    },
                                                    complete: function () {
                                                        $('#loading').css('display', 'none');
                                                    }
                                                });
                                            });

                                            $('#payment').click(function () {
                                                $.ajax({
                                                    url: '/api/payment',
                                                    method: 'post',
                                                    data: {
                                                        'pStudId': $('#ustudentId').val(),
                                                        'rStudId': $('#studentId').val(),
                                                        'semester': $('#semester').val(),
                                                        'otp': $('#otp').val()
                                                    },
                                                    dataType: 'json',
                                                    success: function (sData) {
                                                        alert(sData.message);
                                                        location.reload();
                                                    },
                                                    error: function () {
                                                        console.log('error');
                                                    },
                                                    beforeSend: function () {
                                                        $('#loading').css('display', 'block');
                                                    },
                                                    complete: function () {
                                                        $('#loading').css('display', 'none');
                                                    }
                                                });
                                            });
                                        });
                                    } else {
                                        $('#tuition').html(sHtml);
                                    }
                                }
                            },
                            error: function () {
                                console.log('error');
                            },
                            beforeSend: function () {
                                $('#loading').css('display', 'block');
                            },
                            complete: function () {
                                $('#loading').css('display', 'none');
                            }
                        });
                    } else {
                        $('#tuition').empty();
                    }
                });

            }
        },
        beforeSend: function () {
            $('#loading').css('display', 'block');
        },
        complete: function () {
            $('#loading').css('display', 'none');
        }
    });
});