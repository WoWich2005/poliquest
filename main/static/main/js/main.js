$(function() {
	function getCookieValue(name)
    {
        const regex = new RegExp(`(^| )${name}=([^;]+)`)
        const match = document.cookie.match(regex)
        if (match) {
            return match[2]
        }
    }

	function createErrorAlert(msg) {
		let wrapper = document.createElement('div');
		wrapper.innerHTML = `
			<div id="controllAlert" class="alert alert-warning alert-dismissible fade show" role="alert">
				<h4 class="alert-heading">Ошибка</h4>
				<hr>
				<span class="alert__msg">${msg}</span>
				<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Закрыть"></button>
			</div>
		`;
		
		return wrapper;
	}

	$('.button--send-record').on('click', function() {
		let point_id = this.dataset.point;
		let team_id = $(`.select--team-select[data-point=${point_id}]`).val();
		let action_id = $(`.select--action-select[data-point=${point_id}]`).val();

        let error_block = $(`.errors[data-point=${point_id}]`);
		if(team_id === '-1') {
            $(error_block).html('');
            $(error_block).append(createErrorAlert('Вы не выбрали команду...'));

            return;
        }

        if(action_id === '-1') {
            $(error_block).html('');
            $(error_block).append(createErrorAlert('Вы не выбрали тип действия команды...'));

            return;
        }

		$.ajax({
			url: `/api/v1/points/${point_id}/stats/`,
			method: 'post',
			dataType: 'json',
			data: {
				'point': point_id,
				'team': team_id,
				'type': action_id
			},
			headers: {"X-CSRFToken": getCookieValue('csrftoken')},
			success: function() {
				location.reload();
			},
            error: function(data) {
                $(error_block).html('');
                if(!data["responseJSON"] || !data["responseJSON"]["non_field_errors"]) {
                    $(error_block).append(createErrorAlert('Не удалось отправить данные...'));
                }else{
                    $(error_block).append(
                        createErrorAlert(`${data["responseJSON"]["non_field_errors"]}`)
                    );
                }
            }
		});
	});

	$('.button--edit').on('click', function() {
        let point_id = this.dataset.point
        let record_id = this.dataset.id

		const modal = new bootstrap.Modal(document.getElementById('editStatModal'));

        let team_name = this.dataset.team;
        let datetime = this.dataset.time;

        $(modal._element).find('.edit-record__team').html(team_name);
        $(modal._element).find('.edit-record__datetime').val(datetime);

        let btn = $(modal._element).find('.edit-record__confirm');
        $(btn).off('click');
        $(btn).on('click', function() {
            let datetime = $(modal._element).find('.edit-record__datetime').val();

            $.ajax({
                url: `/api/v1/points/${point_id}/stats/${record_id}`,
                method: 'patch',
                dataType: 'json',
                data: {
                    'time': datetime
                },
                headers: {"X-CSRFToken": getCookieValue('csrftoken')},
                success: function() {
                    location.reload();
                },
                error: function() {
                    let error_block = $(`.errors[data-point=${point_id}]`);

                    modal.hide();
                    $(error_block).html('');
                    $(error_block).append(createErrorAlert('Не удалось изменить запись...'));
                }
            });
        });

        modal.show();
	});

	$('.button--delete').on('click', function() {
        let point_id = this.dataset.point;
        let record_id = this.dataset.id;

		const modal = new bootstrap.Modal(document.getElementById('deleteStatModal'));

        let btn = $(modal._element).find('.btn--confirm')
        $(btn).off('click');
        $(btn).on('click', function() {
            $.ajax({
                url: `/api/v1/points/${point_id}/stats/${record_id}`,
                method: 'delete',
                dataType: 'json',
                headers: {"X-CSRFToken": getCookieValue('csrftoken')},
                success: function() {
                    location.reload();
                },
                error: function() {
                    let error_block = $(`.errors[data-point=${point_id}]`);

                    modal.hide();
                    $(error_block).html('');
                    $(error_block).append(createErrorAlert('Не удалось удалить запись...'));
                }
            });
        });

        modal.show();
	});

	const tabs = document.querySelectorAll('button[data-bs-toggle="tab"]');

	tabs.forEach(tab => {
		tab.addEventListener('shown.bs.tab', (event) => {
			const { target } = event;
			const { id: targetId } = target;
			
			saveTabId(targetId);
		});
	});

	const saveTabId = (selector) => {
		if (history.pushState) {
			let baseUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
			let newUrl = baseUrl + `?tab=${selector}`;
			history.pushState(null, null, newUrl);
            $(".tabs-select").val(selector);
		}
	};

	const getTabId = () => {
		const activeTabId = new URLSearchParams(window.location.search).get('tab');
		
		if (!activeTabId) {
			const tab = new bootstrap.Tab(tabs[0]);
			tab.show();
		}else{
			$('.tabs-select--mobile').val(activeTabId);

			const tab = new bootstrap.Tab(document.querySelector(`#${activeTabId}`));
			tab.show();
		}
	};

	getTabId();

	$('.tabs-select--mobile').on('change', function() {
		let targetId = this.value;
		saveTabId(targetId);
		getTabId();
	});

    $('.map-data').each(function() {
        if($(this).data('not-empty') === true) {
            let id = $(this).data('point-id');
            $(`.map__svg .cls-1[data-point-id=${id}]`).addClass('clickable');
        }
    });

    $(".map__svg polygon.clickable").click(
		function (e) {
            $('.map polygon').removeClass('active');
            $(this).addClass('active');

            let build_info = $('.map__build-info').addClass('active');
            let map_content = $('.map__content');

            let parentOffset = $(map_content).offset();
            let relX = e.clientX - parentOffset.left;
            let relY = e.clientY - parentOffset.top;

			build_info.css('top', Math.min(
                $(map_content).height() - $(build_info).height(),
                Math.max(5, relY + window.scrollY - $(build_info).height() - 30)
            ) + "px");

            build_info.css('left', Math.min(
                $(map_content).width() - $(build_info).width() - 25,
                Math.max(5, relX - ($(build_info).width() / 2))
            ) + "px");

            let point_id = $(this).data('point-id');
            let data = $(`.map__data .map-data[data-point-id=${point_id}]`).clone();
            $(build_info).html('');
            $(build_info).append(data);
		}
	);

    $(window).on('resize', function() {
        $('.map__build-info').removeClass('active');
        $('.map polygon').removeClass('active');
    })

    $(document).on('click', function (e) {
        if (!$(e.target).closest("polygon.clickable").length && !$(e.target).closest(".map__build-info").length) {
            $('.map__build-info').removeClass("active");
            $('.map polygon').removeClass('active');
        }
        e.stopPropagation();
    });

});