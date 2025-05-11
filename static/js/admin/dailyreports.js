var installationData = null;

$(function () {

  formSubmit = true;

  showToggleSearchBtn();

  fill_dataTable();

})

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
      "url": baseUrl + "appinstallations/app_installation_table_data/?datatable=true",
      "type": "POST",
      "dataFilter": function (reps) {
        installationData = JSON.parse(reps);
        return reps;
      }
    },
    createdRow: function (row, data, dataIndex) {
      $(row).data('id', data.appi_id);
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
        "data": "appi_id",
        "render": $.fn.dataTable.render.text()
      },
      {
        "data": "appi_uniqid",
        "render": $.fn.dataTable.render.text()
      },
      {
        "data": "appi_catg",
        "render": $.fn.dataTable.render.text()
      },
      {
        "data": "appi_device_act",
        render: function (data) {
          return $.fn.dataTable.render.text().display(data);
        }
      },
      {
        "data": "appi_idate",
        render: function (data) {
          return $.fn.dataTable.render.text().display(convertDateFormater(data, dateformat_type.ServerDate, dateformat_type.DayMonthYear));
        }
      },
      {
        "data": "appi_appversion",
        render: function (data) {
            return $.fn.dataTable.render.text().display(data);
          }
      },
      {
        "data": "appi_devicetype",
        render: function (data) {
            return $.fn.dataTable.render.text().display(data);
          }
      },
      {
        "data": "appi_deviceos",
        render: function (data) {
            return $.fn.dataTable.render.text().display(data);
          }
      },
    ]
  });

}

$('#table_content tbody').on('click', 'tr td:nth-child(n+1):nth-last-child(n+3)', function () {
  centerEditAction(this, forView = true);
});

function clearSearchAction() {

  $('.searchContainer input').val('');
  $('.searchContainer select').val('');
  $('.searchContainer .search_date .datePicker i').removeClass('fa-calendar-times').addClass('fa-calendar-alt');
  
  $('#table_content').DataTable().search('').columns().search('').draw();
}

function searchAction() {

  var table = $('#table_content').DataTable();

  table.columns(0).search($('.table_search_name').val())
  table.columns(1).search($('.table_search_serviceNo').val())
  table.columns(2).search($('.table_search_email').val())
  table.columns(3).search($('.table_search_mobile').val())
  table.columns(4).search($('.table_search_status').val())
  
  table.draw();
}

function invokeAddOfficerBtnAction() {

  var formEle = '#userForm';

  $(formEle).removeClass('viewOnly')
  $('.userModalHeading').text('Create Police Officer')
  $('.addUserBtn').text('Create')
  $('.addUserBtn').data('id', null)

  resetForm(formEle)

  $(formEle+' .inputNameLabel').addClass('active')
                          
  $('#addUserModal').modal('open')
}

function addUserAction() {

  var formEle = '#userForm'

  if( $('.addUserBtn').text() == 'Edit') {

    removeViewMode(formEle)
    $('.addUserBtn').text('Update')
    $('.userModalHeading').text('Edit Officer Details')
    $('.editSubDivisionBtn').addClass('d-none')

  } else if (validateForm(formEle)) {

    var userForm = document.getElementById("userForm");
    var formData = new FormData(userForm);

    var type = 'POST'
    var id = $('.addUserBtn').data('id')
    if (id != null) {
      formData.append('id', id);
      type = 'PUT'
    }

    $.ajax({
      url: baseUrl + 'officers',
      data: formData,
      cache: false,
      processData: false,
      contentType: false,
      type: type,
      success: function (result) {
        if (apiResStatus(result.status)) {
          $('#table_content').DataTable().draw()
          $('#addUserModal').modal('close')
          show_StatusModal(result.message, result.status)
        } else {
          show_StatusModal(result.message, result.status)
        }
      },
      error: errorCallBack
    });
  }

}

function centerEditAction(ele, forView = false) {

  var id = $(ele).closest('tr').data('id')
  var arr = $.grep(installationData.data, function (obj) {
    return obj.appi_id == id;
  });

  if (arr.length > 0) {
    setSubDivisionDetails(arr[0], forView)
    $('#addUserModal').modal('open')
  }

}

function setSubDivisionDetails(data, forView) {

  $('.userModalHeading').text(forView ? 'Installation Details' : 'Edit Installation Details')
  $('.addUserBtn').text(forView ? 'Edit' : 'Update')
  forView ? $('.editSubDivisionBtn').removeClass('d-none') : $('.editSubDivisionBtn').addClass('d-none')
  $('.addUserBtn').data('id', data.ofcr_id)

  var formEle = '#userForm'
  resetForm(formEle)

  setTimeout(function () {
    $(formEle + ' input[name=uniqueid]').val(data.appi_uniqid)
    $(formEle + ' input[name=catg]').val(data.appi_catg)
    $(formEle + ' input[name=deviceact]').val(data.appi_device_act)
    $(formEle + ' input[name=appversion]').val(data.appi_appversion)
    $(formEle + ' input[name=devicetype]').val(data.appi_devicetype)
    $(formEle + ' input[name=devicemodel]').val(data.appi_devicemodel)
    $(formEle + ' input[name=devicemake]').val(data.appi_devicemake)
    $(formEle + ' input[name=deviceos]').val(data.appi_deviceos)
    $(formEle + ' input[name=deviceosversion]').val(data.appi_deviceosversion)
    $(formEle + ' textarea[name=fcmtoken]').val(data.appi_pntoken)

    checkViewMode(formEle, forView)

  }, 500);
}

function centerDeleteAction(ele) {

  conformationDialog('Confirmation', 'Are you sure to delete.', 'Cancel', 'Delete', function (conformation) {
    if (!conformation) return;
	
    var payload = {
      id: $(ele).closest('tr').data('id')
    }

    $.ajax({
      url: baseUrl + 'officers',
      type: "DELETE",
      contentType: "application/json",
      dataType: 'json',
      data: JSON.stringify(payload),
      success: function (result) {
        if (apiResStatus(result.status)) {
          $('#table_content').DataTable().draw()
          show_StatusModal(result.message, result.status)
        } else {
          show_StatusModal(result.message, result.status)
        }
      },
      error: errorCallBack
    });
    
  })
}

function updateStatusAction(id, status) {

  var payload = {
    id: id,
    status: status
  }

  $.ajax({
    url: baseUrl + 'officers',
    type: "PATCH",
    contentType: "application/json",
    dataType: 'json',
    data: JSON.stringify(payload),
    success: function (result) {
      if (apiResStatus(result.status)) {
        $('#table_content').DataTable().draw()
        show_StatusModal(result.message, result.status)
      } else {
        show_StatusModal(result.message, result.status)
      }
    },
    error: errorCallBack
  });

}