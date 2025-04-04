
var usersData = null


$(function () {

  formSubmit = true;
  $('.search_date .date-field').datepicker({
    format: dateformat_type.DisplayDate_Small,
    autoclose: true
  }).on('changeDate', function (e) {
    $(this).parent().find('.datePicker i').removeClass('fa-calendar-alt').addClass('fa-calendar-times');
  });
  fill_dataTable();
})


function confirmDialog_Actions() {

  $('[data-toggle=confirmation]').confirmation({
    rootSelector: '[data-toggle=confirmation]',
    onConfirm: function () {
      var id = $(this).parents('tr').data('id');
      var status = $(this).data('value');

      switch (status) {
        case 'AC':
          updateStatusAction(id, 'NA');
          break;
        case 'NA':
          updateStatusAction(id, 'AC');
          break;
      }
    },
    onCancel: function () {
    }
  });

}

function fill_dataTable() {
  var table = $('#table_content').DataTable({
    "drawCallback": function (settings) {
      confirmDialog_Actions();
    },
    "fnRowCallback": function (nRow, aData, iDisplayIndex) {
      var oSettings = this.fnSettings();
      $("td:first", nRow).html(oSettings._iDisplayStart + iDisplayIndex + 1);
      return nRow;
    },
    "bLengthChange": false,
    "processing": true,
    "serverSide": true,
    "ajax": {
      "url": baseUrl + "users/approved/?datatable=true",
      "type": "POST",
      "dataFilter": function (reps) {
        usersData = JSON.parse(reps);
        return reps;
      }
    },
    createdRow: function (row, data, dataIndex) {
      $(row).data('id', data.cusr_id);
    },
    "columnDefs": [
      {
        "targets": '_all',
        "render": $.fn.dataTable.render.text()
      },
      {
        'targets': [7], /* column index */
        'orderable': false, /* true or false */
      }
    ],
    "columns": [
      {
        "data": "cusr_id",
        "render": $.fn.dataTable.render.text()
      },
      {
        "data": "cusr_full_name",
        "render": $.fn.dataTable.render.text()
      },
      {
        "data": "cusr_email",
        "render": $.fn.dataTable.render.text()
      },
      {
        "data": "cusr_mobile",
        render: function (data) {
          return $.fn.dataTable.render.text().display(data);
        }
      },
      {
        "data": "cusr_created_at",
        render: function (data) {
          return $.fn.dataTable.render.text().display(convertDateFormater(data, dateformat_type.ServerDate, dateformat_type.DayMonthYear));
        }
      },
      {
        "data": "cusr_last_login_timestamp",
        render: function (data) {
          return $.fn.dataTable.render.text().display(convertDateFormater(data, dateformat_type.ServerDate, dateformat_type.DayMonthYear));
        }
      },
      {
        "data": "cusr_status",
        render: function (data) {
          var btn_type = (data === 'AC') ? 'btn-success' : 'btn-danger';
          var status = (data === 'AC') ? 'Active' : 'Not Active';
          return $('<div>').append($('<button />')
            .prop('type', 'button')
            .prop('class', 'btn ' + btn_type + ' btn_cstm_status')
            .css('width', '90px')
            .attr('data-value', data)
            .attr('data-toggle', 'confirmation')
            .attr('data-popout', 'true')
            .attr('data-singleton', 'true')
            .attr('data-btn-ok-label', 'Yes')
            .attr('data-btn-cancel-label', 'No')
            .attr('data-title', 'Change User status')
            .text(fetchbuttonEnum(data))).html();
        }
      },
      {
        "class": "text-center",
        "data": null,
        "render": function (data, type, row) {
          return `<a class="tableActionBtn" href="javascript:void(0)" onclick="recordEditAction(this)"><i class="fa fa-edit"></i></a>
                    <a class="tableActionBtn" href="javascript:void(0)" onclick="recordDeleteAction(this)"><i class="fa fa-trash-alt"></i></a>
                    <a class="tableActionBtn" href="javascript:void(0)" onclick="invokeResetPasswordBtnAction(this)"><i class="fa fa-key"></i></a>`;
        }
      }
    ]
  });

}

$('#table_content tbody').on('click', 'tr td:nth-child(n+1):nth-last-child(n+3)', function () {
  recordEditAction(this, forView = true);
});


function invokeResetPasswordBtnAction(ele) {


  var id = $(ele).closest('tr').data('id')

  var arr = $.grep(usersData.data, function (obj) {
    return obj.id == id;
  });

  if (arr[0].ausr_status == 'DL') {
    show_StatusModal('Cannot Perform Change Password Action On Deleted User', "error")
    return
  }
  $('.resetPwdBtn').data('id', $(ele).closest('tr').data('id'))
  // $('.resetPwdBtn').data('org_id', $(ele).closest('tr').data('org_id'))
  resetForm('#resetPwdForm')
  $('#resetPwdModal').modal('show')

}

function resetPasswordAction() {

  var formEle = '#resetPwdForm'

  if (validateForm(formEle)) {

    var recordForm = document.getElementById("resetPwdForm");
    var formData = new FormData(recordForm);

    formData.set('password', rsa_encrypt.encrypt(formData.get('password')));

    formData.append('id', $('.resetPwdBtn').data('id'));


    $.ajax({
      url: baseUrl + 'reset_password/',
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      type: 'PATCH',
      success: function (result) {
        if (apiResStatus(result.status)) {
          $('#table_content').DataTable().draw()
          $('#resetPwdModal').modal('hide')
        }
        show_StatusModal(result.message, result.status)
      },
      error: errorCallBack
    });

  }

}


function clearSearchAction() {

  $('.searchContainer input').val('');
  $('.searchContainer select').val('');
  $('.searchContainer .search_date .datePicker i').removeClass('fa-calendar-times').addClass('fa-calendar-alt');

  $('#table_content').DataTable().search('').columns().search('').draw();
}

function fetchbuttoncolor(val) {
  if (val == 'AC') {
    return 'btn-success'
  }
  if (val == 'NA') {
    return 'btn-warning'
  }
  if (val == 'DL') {
    return 'btn-danger'
  }
}

function fetchbuttonEnum(val) {
  if (val == 'AC') {
    return 'Active'
  }
  if (val == 'NA') {
    return 'Not Active'
  }
  if (val == 'DL') {
    return 'Deleted'
  }
}

function searchAction() {

  var table = $('#table_content').DataTable();

  var from_date = convertDateFormater($('.table_search_startdate').val(), dateformat_type.DisplayDate, dateformat_type.ServerDate)
  var to_date = convertDateFormater($('.table_search_enddate').val(), dateformat_type.DisplayDate, dateformat_type.ServerDate)
  
  table.columns(0).search($('.table_search_fname').val())
  table.columns(1).search($('.table_search_lname').val())
  table.columns(2).search($('.table_search_username').val())
  table.columns(3).search($('.table_search_designation').val())
  table.columns(4).search($('.table_search_startdate').val())
  table.columns(5).search($('.table_search_enddate').val())
  table.columns(6).search($('.table_search_status').val())

  table.draw();
}

function invokeAddRecordBtnAction() {

  var formEle = '#recordForm';

  $(formEle).removeClass('viewOnly')
  $('.recordModalHeading').text('Add User')
  $('.editRecordBtn').addClass('d-none')
  $('.addRecordBtn').text('Add')
  $('.addRecordBtn').data('id', null)
  $('.addRecordBtn').data('org_id', null)

  $(formEle + ' select[name=organization]').prop('disabled', false)
  $(formEle + ' input[name=password]').prop('required', true)
  $('.passwordCol input[name=password]').prop('disabled', false).addClass("mandatoryLocal")

  resetForm(formEle)

  // $('#admin-console-opts-div').addClass('d-none')
  $('#operator-console-opts-div').addClass('d-none')

  $('#addRecordModal').modal('show')
}

function addRecordAction() {
  alert(baseUrl + 'user/')

  var formEle = '#recordForm'

  if ($('.addRecordBtn').text() == 'Edit') {

    removeViewMode(formEle)
    $('.addRecordBtn').text('Update')
    $('.recordModalHeading').text('Edit User')
    $('.editRecordBtn').addClass('d-none')

  } else if (validateForm(formEle)) {

    var recordForm = document.getElementById("recordForm");
    var formData = new FormData(recordForm);
    var optionsList = []

    $('.preferenceCheckBox:checked').each(function (index, obj) {
      optionsList.push($(this).data('id'))
    })

    formData.append('optionsList', JSON.stringify(optionsList));
    formData.set('password2', rsa_encrypt.encrypt(formData.get('password')));

    var type = 'POST'
    var id = $('.addRecordBtn').data('id')

    if (!isInvalidString(id)) {
      formData.append('id', id);
      formData.delete('password');
      formData.delete('password2');
      type = 'PUT'
    } else {
      formData.set('password', rsa_encrypt.encrypt(formData.get('password')));
    }

    $.ajax({
      url: baseUrl + 'user/',
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      type: type,
      success: function (result) {
        if (apiResStatus(result.status)) {
          $('#table_content').DataTable().draw()
          $('#addRecordModal').modal('hide')
        }
        show_StatusModal(result.message, result.status)
      },
      error: errorCallBack
    });
  }

}

function updateStatusAction(id, status) {

  var payload = {
    id: id,
    status: status
  }

  $.ajax({
    url: baseUrl + 'change_status/',
    type: "PATCH",
    contentType: "application/json",
    dataType: 'json',
    data: JSON.stringify(payload),
    success: function (result) {
      if (apiResStatus(result.status)) {
        $('#table_content').DataTable().draw()
      }
      show_StatusModal(result.message, result.status)
    },
    error: errorCallBack
  });

}

function recordDeleteAction(ele) {

  var id = $(ele).closest('tr').data('id')

  var org_id = $(ele).closest('tr').data('org_id')

  var arr = $.grep(usersData.data, function (obj) {
    return obj.id == id;
  });

  if (arr[0].ausr_status == 'DL') {
    show_StatusModal('Cannot Perform Delete Action On Deleted User', "error")
    return
  }

  show_conformationModal({ message: "Are you sure to delete this User?" }, function (conformation) {
    if (!conformation) return;

    var payload = {
      id: id
    }

    $.ajax({
      url: baseUrl + 'user/',
      type: "DELETE",
      contentType: "application/json",
      dataType: 'json',
      data: JSON.stringify(payload),
      success: function (result) {
        if (apiResStatus(result.status)) {
          $('#table_content').DataTable().draw()
        }
        show_StatusModal(result.message, result.status)
      },
      error: errorCallBack
    });
  })

}

function recordEditAction(ele, forView = false) {

  var id = $(ele).closest('tr').data('id')
  // var org_id = $(ele).closest('tr').data('org_id')
  var arr = $.grep(usersData.data, function (obj) {
    return obj.id == id;
  });
  if (arr[0].ausr_status == 'DL' && !forView) {
    show_StatusModal('Cannot Perform Update Action On Deleted User', "error")
    return
  }
  if (arr.length > 0) {
    setRecordDetails(arr[0], forView)
    $('#addRecordModal').modal('show')
  }

}

function setRecordDetails(data, forView) {

  $('.recordModalHeading').text(forView ? 'User' : 'Edit User')
  $('.addRecordBtn').text(forView ? 'Edit' : 'Update')
  forView ? $('.editRecordBtn').removeClass('d-none') : $('.editRecordBtn').addClass('d-none')
  $('.addRecordBtn').data('id', data.id)
  $('.addRecordBtn').data('org_id', data.orgn_id)

  var formEle = '#recordForm'
  resetForm(formEle)
  $('.preferenceCheckBox').prop("checked", false)
  $.each(data.options, function (index, id) {

    $('.preferenceCheckBox[data-id="' + id + '"]').prop("checked", true)
  })
  $(formEle + ' input[name=username]').val(data.username)
  // $(formEle + ' select[name=organization]').val(data.orgn_id)
  // $(formEle + ' select[name=organization]').prop('disabled', true)
  $(formEle + ' select[name=user_type]').val(data.user_type)
  $(formEle + ' input[name=user_firstname]').val(data.user_firstname)
  $(formEle + ' input[name=user_lastname]').val(data.user_lastname)
  $(formEle + ' input[name=user_desg]').val(data.user_desg)
  $(formEle + ' input[name=email]').val(data.email)
  $(formEle + ' input[name=user_mobile]').val(data.user_mobile)

  // $(formEle + ' input[name=password]').prop('required', false)
  $('.passwordCol input[name=password]').prop('disabled', true).prop('required', false).val("********").removeClass("mandatoryLocal")

  checkViewMode(formEle, forView)
}


