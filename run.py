import discord
import asyncio
import re
import os, random, time

from discord import Client

client: = Client discord.Client()

# 사용하는 변수들
idA, moneyA, timeA, give, ID, TIME = [], [], [], 0, 0, 0
ment = ["배수 정하는 중.", "배수 정하는 중..", "배수 정하는 중..."]

try:  # 만약 파일이 없으면 새로 만듦
    f = open("UserData.txt", "r")
except:
    f = open("UserData.txt", "w")
    f.close()
    f = open("UserData.txt", "r")
while True:  # 유저들 데이터를 읽음 데이터 형식 : 유저ID,가지고 있는 돈,돈받은 시간
    line = f.readline()
    if not line: break
    line = line.split(",")
    idA.append(line[0])
    moneyA.append(int(line[1]))
    timeA.append(int(line[2]))
f.close()


@client.event
async def on_ready():  # 봇이 켜지면
    print("dd: ", client.user.id)
    print("봇 준비 완료")
    game = discord.Game("!도움말")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    if message.content == "!돈받기":
        ID = str(message.author.id)
        TIME = int(time.time())
        if ID in idA:  # 만약 등록된 ID라면
            if TIME - timeA[idA.index(ID)] < 30:  # 1시간이 안 지났을 때
                embed = discord.Embed(title='', description='30초 마다 받을 수 있습니다.', color=0xFF0000)
                await message.channel.send(embed=embed)
                raise ValueError  # 탈출
            elif TIME - timeA[idA.index(ID)] >= 30:  # 1시간이 지났을 때
                timeA[idA.index(ID)] = int(time.time())
        give = random.randrange(1, 10) * random.randrange(1000, 10000)  # 줄 돈
        if ID in idA:
            moneyA[idA.index(ID)] += give
            f = open("UserData.txt", "w")  # 저장
            for i in range(0, len(idA), 1):
                f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
            f.close()
        elif not ID in idA:
            idA.append(ID)
            moneyA.append(give)
            timeA.append(int(time.time()))
            f = open("UserData.txt", "w")  # 저장
            for i in range(0, len(idA), 1):
                f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
            f.close()
        msg = str(give) + "원 만큼 받았습니다. 현재 돈: " + str(moneyA[idA.index(ID)]) + "원"
        embed = discord.Embed(title='', description=msg, color=0x00FF00)
        await message.channel.send(embed=embed)
    if message.content.startswith("!도박"):
        ID = str(message.author.id)
        msg = message.content.split()
        if msg[1].isdecimal() == False:  # 만약 숫자가 아니라면
            embed = discord.Embed(title='', description='숫자만 입력해 주세요!', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError
        msg[1] = int(msg[1])
        if not ID in idA or moneyA[idA.index(ID)] - int(msg[1]) < 0:  # 등록된 ID가 아니거나 돈이 부족하면
            embed = discord.Embed(title='', description='돈이 부족합니다!', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError  # 탈출
        moneyA[idA.index(ID)] -= msg[1]
        give = random.randrange(1, 11)
        count = await message.channel.send("배수 정하는 중...")
        for i in range(0, 2):
            await count.edit(content=ment[0])
            await asyncio.sleep(0.2)
            await count.edit(content=ment[1])
            await asyncio.sleep(0.2)
            await count.edit(content=ment[2])
            await asyncio.sleep(0.2)
        await count.edit(content='만약 성공하면 건 돈의 ' + str(give) + "배 를 얻어요")
        await asyncio.sleep(1)
        if give % 2 == 0:
            await count.edit(content="도박 성공!")
            moneyA[idA.index(ID)] += give * msg[1]
            await asyncio.sleep(0.5)
            await count.edit(content="도박 성공! 현재 돈: " + str(moneyA[idA.index(ID)]) + "원")
        elif give % 2 != 0:
            await count.edit(content="도박 실패...")
            await asyncio.sleep(0.5)
            await count.edit(content="도박 실패... 현재 돈: " + str(moneyA[idA.index(ID)]) + "원")
        f = open("UserData.txt", "w")  # 저장
        for i in range(0, len(idA), 1):
            f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
        f.close()

    if message.content == "!돈":
        ID = str(message.author.id)
        if ID in idA:  # 만약 등록된 ID라면
            embed = discord.Embed(title='', description=str(moneyA[idA.index(ID)]) + " 원", color=0x118811)
            await message.channel.send(embed=embed)
        elif not ID in idA:  # 등록된 ID가 아니라면
            embed = discord.Embed(title='', description="0 원", color=0x118811)
            await message.channel.send(embed=embed)

    if message.content == "!도움말":
        embed = discord.Embed(title="명령어", description="봇 명령어", color=0x62c1cc)
        embed.add_field(name="도박", value="돈, 돈받기, 도박 <금액>, 올인, 랭킹", inline=True)
        await message.channel.send('', embed=embed)

    if message.content == "!올인":
        ID = str(message.author.id)
        if not ID in idA or moneyA[idA.index(ID)] <= 0:  # 만약 돈이 부족하면
            embed = discord.Embed(title='', description='돈이 부족합니다.', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError
        give = random.randrange(2, 10)
        count = await message.channel.send("배수 정하는 중...")
        for i in range(0, 2):
            await count.edit(content=ment[0])
            await asyncio.sleep(0.2)
            await count.edit(content=ment[1])
            await asyncio.sleep(0.2)
            await count.edit(content=ment[2])
            await asyncio.sleep(0.2)
        await count.edit(content='만약 성공하면 건 돈의 ' + str(give) + "배 를 얻어요")
        await asyncio.sleep(1)
        if give % 2 == 0:
            await count.edit(content="올인 성공!")
            moneyA[idA.index(ID)] *= give
            await asyncio.sleep(0.5)
            await count.edit(content="올인 성공! 현재 돈: " + str(moneyA[idA.index(ID)]) + "원")
        elif give % 2 != 0:
            await count.edit(content="올인 실패...")
            moneyA[idA.index(ID)] = 0
            await asyncio.sleep(0.5)
            await count.edit(content="올인 실패... 현재 돈: " + str(moneyA[idA.index(ID)]) + "원")
        f = open("UserData.txt", "w")  # 저장
        for i in range(0, len(idA), 1):
            f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
        f.close()

    if message.content == "!랭킹":
        rank, rankA = "", []
        for i in range(0, len(idA)): rankA.append([idA[i], moneyA[i]])
        rankA = sorted(rankA, reverse=True, key=lambda x: x[1])  # 많은 순으로 정렬
        for i in range(0, 10):  # 10위 까지만 출력
            try:
                rank += str(i + 1) + "위 <@" + rankA[i][0] + "> : " + str(rankA[i][1]) + "\n"
            except:
                break
        embed = discord.Embed(title='돈 랭킹', description=rank, color=0xd8aa2d)
        await message.channel.send(embed=embed)


client.run("Nzg2MjQ3NTU3NTI0NzUwMzM2.X9DoGQ.3_ayPy51EPdrk-jXEzzRbZYl17Q")import discord
import asyncio
import re
import os, random, time

client = discord.Client()

#사용하는 변수들
idA, moneyA, timeA, give, ID, TIME =  [], [], [], 0, 0, 0
ment = ["배수 정하는 중.", "배수 정하는 중..", "배수 정하는 중..."]

try: #만약 파일이 없으면 새로 만듦
    f = open("UserData.txt", "r")
except:
    f = open("UserData.txt", "w")
    f.close()
    f = open("UserData.txt", "r")
while True: #유저들 데이터를 읽음 데이터 형식 : 유저ID,가지고 있는 돈,돈받은 시간
    line = f.readline()
    if not line: break
    line = line.split(",")
    idA.append(line[0])
    moneyA.append(int(line[1]))
    timeA.append(int(line[2]))
f.close()

@client.event
async def on_ready(): #봇이 켜지면
    print("dd: ", client.user.id)
    print("봇 준비 완료")
    game = discord.Game("!도움말")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.content == "!돈받기":
        ID = str(message.author.id)
        TIME = int(time.time())
        if ID in idA: #만약 등록된 ID라면
            if TIME - timeA[idA.index(ID)] < 30: #1시간이 안 지났을 때
                embed = discord.Embed(title='', description='30초 마다 받을 수 있습니다.', color=0xFF0000)
                await message.channel.send(embed=embed)
                raise ValueError #탈출
            elif TIME - timeA[idA.index(ID)] >= 30: #1시간이 지났을 때
                timeA[idA.index(ID)] = int(time.time())
        give = random.randrange(1,10)*random.randrange(1000,10000) # 줄 돈
        if ID in idA:
            moneyA[idA.index(ID)] += give
            f = open("UserData.txt", "w") #저장
            for i in range(0,len(idA),1):
                f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
            f.close()
        elif not ID in idA:
            idA.append(ID)
            moneyA.append(give)
            timeA.append(int(time.time()))
            f = open("UserData.txt", "w") #저장
            for i in range(0,len(idA),1):
                f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
            f.close()
        msg = str(give)+"원 만큼 받았습니다. 현재 돈: "+str(moneyA[idA.index(ID)])+"원"
        embed = discord.Embed(title='', description=msg, color=0x00FF00)
        await message.channel.send(embed=embed)
    if message.content.startswith("!도박"):
        ID = str(message.author.id)
        msg = message.content.split()
        if msg[1].isdecimal() == False: #만약 숫자가 아니라면
            embed = discord.Embed(title='', description='숫자만 입력해 주세요!', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError
        msg[1] = int(msg[1])
        if not ID in idA or moneyA[idA.index(ID)] - int(msg[1]) < 0: #등록된 ID가 아니거나 돈이 부족하면
            embed = discord.Embed(title='', description='돈이 부족합니다!', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError #탈출
        moneyA[idA.index(ID)] -= msg[1]
        give = random.randrange(1,11)
        count = await message.channel.send("배수 정하는 중...")
        for i in range(0,2):
            await count.edit(content = ment[0])
            await asyncio.sleep(0.2)
            await count.edit(content = ment[1])
            await asyncio.sleep(0.2)
            await count.edit(content = ment[2])
            await asyncio.sleep(0.2)
        await count.edit(content = '만약 성공하면 건 돈의 '+str(give)+"배 를 얻어요")
        await asyncio.sleep(1)
        if give % 2 == 0:
            await count.edit(content = "도박 성공!")
            moneyA[idA.index(ID)] += give*msg[1]
            await asyncio.sleep(0.5)
            await count.edit(content = "도박 성공! 현재 돈: "+str(moneyA[idA.index(ID)])+"원")
        elif give % 2 != 0:
            await count.edit(content = "도박 실패...")
            await asyncio.sleep(0.5)
            await count.edit(content = "도박 실패... 현재 돈: "+str(moneyA[idA.index(ID)])+"원")
        f = open("UserData.txt", "w") #저장
        for i in range(0,len(idA),1):
            f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
        f.close()

    if message.content == "!돈":
        ID = str(message.author.id)
        if ID in idA: #만약 등록된 ID라면
            embed = discord.Embed(title='', description=str(moneyA[idA.index(ID)])+" 원", color=0x118811)
            await message.channel.send(embed=embed)
        elif not ID in idA: #등록된 ID가 아니라면
            embed = discord.Embed(title='', description="0 원", color=0x118811)
            await message.channel.send(embed=embed)

    if message.content == "!도움말":
        embed = discord.Embed(title="명령어", description="봇 명령어", color=0x62c1cc)
        embed.add_field(name="도박", value="돈, 돈받기, 도박 <금액>, 올인, 랭킹", inline=True)
        await message.channel.send('', embed=embed)

    if message.content == "!올인":
        ID = str(message.author.id)
        if not ID in idA or moneyA[idA.index(ID)] <= 0: #만약 돈이 부족하면
            embed = discord.Embed(title='', description='돈이 부족합니다.', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError
        give = random.randrange(2,10)
        count = await message.channel.send("배수 정하는 중...")
        for i in range(0,2):
            await count.edit(content = ment[0])
            await asyncio.sleep(0.2)
            await count.edit(content = ment[1])
            await asyncio.sleep(0.2)
            await count.edit(content = ment[2])
            await asyncio.sleep(0.2)
        await count.edit(content = '만약 성공하면 건 돈의 '+str(give)+"배 를 얻어요")
        await asyncio.sleep(1)
        if give % 2 == 0:
            await count.edit(content = "올인 성공!")
            moneyA[idA.index(ID)]*= give
            await asyncio.sleep(0.5)
            await count.edit(content = "올인 성공! 현재 돈: "+str(moneyA[idA.index(ID)])+"원")
        elif give % 2 != 0:
            await count.edit(content = "올인 실패...")
            moneyA[idA.index(ID)] = 0
            await asyncio.sleep(0.5)
            await count.edit(content = "올인 실패... 현재 돈: "+str(moneyA[idA.index(ID)])+"원")
        f = open("UserData.txt", "w") #저장
        for i in range(0,len(idA),1):
            f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
        f.close()

    if message.content == "!랭킹":
        rank, rankA = "", []
        for i in range(0,len(idA)): rankA.append([idA[i], moneyA[i]])
        rankA = sorted(rankA, reverse = True, key = lambda x: x[1]) #많은 순으로 정렬
        for i in range(0,10): #10위 까지만 출력
            try:
                rank += str(i+1)+"위 <@"+rankA[i][0]+"> : "+str(rankA[i][1])+"\n"
            except:
                break
        embed = discord.Embed(title='돈 랭킹', description=rank, color=0xd8aa2d)
        await message.channel.send(embed=embed)

client.run("Nzg2MjQ3NTU3NTI0NzUwMzM2.X9DoGQ.3_ayPy51EPdrk-jXEzzRbZYl17Q")