import json  # to open json file
import datetime  # to calculate meals during a time period

# encoding="utf-8" if data contains any non ASCII character
json_file = open("7.json", "r", encoding="utf-8")  # import Json File
# identify current file
working_with = 7

# store all UserId to check is User valid or not
ListofuserId = [7, 2, 2627, 10780, 13116, 20566, 21632, 27366, 29127, 30024, 30332, 31870, 33550, 34407, 34429, 36495,
                37327, 38639]

# Load the Json Data
original_file = json.load(json_file)


### Section to find out activeness of user for a specific period of time
def activeness():
    """
    # Comment out and run to see all the Date

    store_date = original_file['calendar']['dateToDayId']
    for it in store_date:
        print(it)

    """
    From_date_temp = input("Enter Initial valid Date (Format Example: \"2016-07-14\") : ")

    # check weather input Date is valid or in right format or not
    store_date = original_file['calendar']['dateToDayId']
    present = 0
    for it in store_date:
        if From_date_temp == it:
            present = 1
            break
    while present == 0:
        From_date_temp = input(
            "Invalid Format or incorrect Date. Please provide a Valid one (Format Example: \"2016-07-14\") : ")
        for it in store_date:
            if From_date_temp == it:
                present = 1
                break



    To_date_temp = input("Enter final valid Date: (Format Example: \"2016-09-24\") : ")
    present_1 = 0
    for it in store_date:
        if To_date_temp == it:
            present_1 = 1
            break
    while present_1 == 0:
        To_date_temp = input("Invalid Format or incorrect Date. Please provide a Valid one (Format Example: \"2016-09-24\") : ")
        for it in store_date:
            if To_date_temp == it:
                present_1 = 1
                break

    # Convert Date (String) into int and Store them onto three different Variable
    From_date_year, From_date_month, From_date_day = map(int, From_date_temp.split('-'))
    To_date_year, To_date_month, To_date_day = map(int, To_date_temp.split('-'))

    # Convert three Int (Year,Date,Month) into dateTime format
    From_date = datetime.datetime(From_date_year, From_date_month, From_date_day)
    To_date = datetime.datetime(To_date_year, To_date_month, To_date_day)

    """
     As Here, all file's UserId is unique but it is possible that we will work in future
     in a single file where UserId can be different , In that case we need to take specific user

    """

    print("Please Enter UserID (Must a integer value): Your Current Id is ", working_with, end=' ')
    User_id = int(input(": "))

    # check weather User is valid or not
    # these portion of code will need if we work with many user with a single file
    present_3 = 0
    if User_id ==  working_with:
        present_3 = 1
    while present_3 == 0:
        if User_id != working_with:
            #as we are working with a single file and we know which file it is
            # that's why we set userId as file id manually
            User_id = working_with
            present_3 = 1
            print(" Your UserId is set to ", working_with," manually ")
            break
        print("Please Enter UserID (Must be a integer value): Your Current Id is ", working_with, end=' ')
        User_id = int(input(": "))


    # this section is to check validity of user ( Reserve to work in future).
    if User_id == working_with:
        present_3 = 1
    while present_3 == 0:
        User_id = int(input("Invalid Format or incorrect User Id. Please Enter UserID (Must a integer value): "))
        for it in ListofuserId:
            if User_id == it:
                present_3 = 1
                break



    list_of_UserIdRelated_Date = []
    List_of_DayId_on_meal = []

    # Here we are finding UserId under Date
    for it in original_file['calendar']['daysWithDetails']:
        temp = original_file['calendar']['daysWithDetails'][it]['day']['userId']
        if temp == User_id:
            list_of_UserIdRelated_Date.append(original_file['calendar']['daysWithDetails'][it]['day']['id'])

    """
    It is possible that a single Date belongs to multiple meal
    And all meals were not taken by user
    Fot that, we need all meals those are taken by any user and store them in a list 
    """
    for it_1 in original_file['calendar']['mealIdToDayId']:
        meal_with_date = original_file['calendar']['mealIdToDayId'][it_1]
        for it_2 in list_of_UserIdRelated_Date:
            if it_2 == meal_with_date:
                List_of_DayId_on_meal.append(meal_with_date)
                break

    """
    Now count total number of meal taken by a user  between two Date
    and Print out Activeness considering the given threshold 

    """

    Total_Meal_Count = 0
    for it_1 in original_file['calendar']['dateToDayId']:
        for it_2 in List_of_DayId_on_meal:
            if it_2 == original_file['calendar']['dateToDayId'][it_1]:
                Int_year, Int_month, Int_day = map(int, it_1.split('-'))
                Meal_time = datetime.datetime(Int_year, Int_month, Int_day)

                if From_date <= Meal_time <= To_date:
                    Total_Meal_Count += 1
                break

    print()
    print()
    check_active = 0
    # if Total_meal_Count is atleast 5 this user is Active
    if Total_Meal_Count > 4:
        check_active = 1
        print(User_id, ' active ', From_date_temp, ' ', To_date_temp)

    # if Total_meal_Count is more than 10 this user is SuperActive
    elif Total_Meal_Count > 10:
        check_active = 1
        print(User_id, ' superactive ', From_date_temp, ' ', To_date_temp)

    ###Section to Calculate total Bored User
    ## fist find out the oldest date among all date then calulate number of meals during preceding period

    # initialize every value with big value to find out minimum one
    Oldest_year = 50000
    Oldest_month = 50000
    Oldest_day = 50000
    for it_1 in original_file['calendar']['dateToDayId']:
        # here temp = year, a = Month, b = day
        temp, a, b = map(int, it_1.split('-'))
        if temp < Oldest_year:
            Oldest_year = temp
        if temp == Oldest_year and a < Oldest_month:
            Oldest_month = a
        if temp == Oldest_year and a == Oldest_month and b < Oldest_day:
            Oldest_day = b

    Preceding_time = datetime.datetime(Oldest_year, Oldest_month, Oldest_day)
    Total_preceding_Meal = 0
    for it_1 in original_file['calendar']['dateToDayId']:
        for it_2 in List_of_DayId_on_meal:
            if it_2 == original_file['calendar']['dateToDayId'][it_1]:
                Int_year, Int_month, Int_day = map(int, it_1.split('-'))
                Meal_time = datetime.datetime(Int_year, Int_month, Int_day)
                if Preceding_time >= Meal_time:
                    Total_preceding_Meal += 1
                break

    if Total_preceding_Meal > 4 and Total_Meal_Count < 5:
        check_active = 1
        print(User_id, ' bored  ', From_date_temp, ' ', To_date_temp)

    if check_active == 0:
        print("Active User is not found ")



    # other section
def mealinaday():
    ### section to find out total number of meal in particular date
    date = input("input Date to  find out total number of  Meal in Particular Date(Format Example: \"2016-08-17\"): ")
    ss = original_file['calendar']['dateToDayId'][date]
    s = original_file.get('calendar', ()).get('dateToDayId', ()).get(ss, "No such Date in Database")

    Date_for_count_meal = input("Enter Valid date to count Number of Meal in this particular day:")
    Meal_count_for_day = 0
    Date_id = original_file['calendar']['dateToDayId'][Date_for_count_meal]

    for i in original_file['calendar']['mealIdToDayId']:
        if Date_id == original_file['calendar']['mealIdToDayId'][i]:
            Meal_count_for_day += 1
    print("Total Meal in ", Date_for_count_meal, " : ", Meal_count_for_day)



activeness()
##to count meal in a day
#mealinaday()
