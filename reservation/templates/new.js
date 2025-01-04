
<script>
    $(document).ready(function () {
        // Sample reserved dates
        const reservedDates = [
            {% for start_date, end_date in reservation_date %}
                { from: '{{ start_date }}', to: '{{ end_date }}' }{% if not forloop.last %},{% endif %}
            {% endfor %}
        ];

        const format = "Y-m-d";

        function getReservedDates() {
            return reservedDates.flatMap(range => {
                const dates = [];
                const start = new Date(range.from);
                const end = new Date(range.to);
                for (let d = start; d <= end; d.setDate(d.getDate() + 1)) {
                    dates.push(new Date(d).toISOString().split('T')[0]);
                }
                return dates;
            });
        }

        const reservedDatesList = getReservedDates();

        function getMaxEndDate(startDate) {
            for (let range of reservedDates) {
                if (new Date(startDate) < new Date(range.from)) {
                    let maxEndDate = new Date(range.from);
                    maxEndDate.setDate(maxEndDate.getDate() - 1);
                    return maxEndDate;
                }
            }
            return null;
        }

        const dateFromPicker = flatpickr("#dateFrom", {
            dateFormat: format,
            disable: reservedDatesList,
            onChange: function(selectedDates, dateStr, instance) {
                const startDate = selectedDates[0];
                const maxEndDate = getMaxEndDate(startDate);
                const dateToPicker = flatpickr("#dateTo", {
                    dateFormat: format,
                    disable: reservedDatesList,
                    minDate: startDate,
                    maxDate: maxEndDate ? maxEndDate : null,
                    onChange: function() {
                        dateToPicker.destroy(); // Destroy to avoid duplicate initialization
                    }
                });
            }
        });

        const dateToPicker = flatpickr("#dateTo", {
            dateFormat: format,
            disable: reservedDatesList,
            onChange: function(selectedDates, dateStr, instance) {
                const endDate = selectedDates[0];
                const dateFromPicker = flatpickr("#dateFrom", {
                    dateFormat: format,
                    disable: reservedDatesList,
                    maxDate: endDate,
                    onChange: function() {
                        dateFromPicker.destroy(); // Destroy to avoid duplicate initialization
                    }
                });
            }
        });
    });
</script>