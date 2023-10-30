import uuid
# campuses = Campus.objects.all().values()
#
# for campuse in campuses:
#     floors = campuse["floors"]
#     camp = Campus.objects.get(id=campuse["id"])
#     for floor in range(floors):
#         fl = Floor(number=floor,campus=camp)
#         fl.save()
#         for i in range(20):
#             take = random.randint(1, 4)
#             amount = random.randint(5, 8)
#             rm = Room(number=i+1,taken_beds=take,num_beds=amount,floor=fl,campus=camp)
#             rm.save()
print(str(uuid.uuid4())[0:5])