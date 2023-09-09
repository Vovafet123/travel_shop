function getData(roomPk) {
    console.log(roomPk)

    let inputStartDate = document.querySelector(`#start-date-${roomPk}`)
    let startDate = inputStartDate.value

    let inputEndDate = document.querySelector(`#end-date-${roomPk}`)
    let endDate = inputEndDate.value

    return startDate, endDate
}