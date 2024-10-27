import glob
import os.path
from datetime import datetime, timedelta

import lingua_franca
import lingua_franca.parse
import lingua_franca.format
import uvicorn
from starlette.responses import FileResponse, JSONResponse
from models import *
from kit import *
from fastapi import FastAPI, File, Query, UploadFile
from config import __version__, api
from typing_extensions import Annotated

lingua_franca.load_languages(["en", "pt"])

userKit = UserKit()
intentKit = IntentKit()
dictionaryKit = DictionaryKit()

app = FastAPI(title="Alex Server", version=__version__, description="Alex api server that handles complex and heavy tasks such an nlp user managements etc.", summary="Alex base server used for handling heavy functions", contact={"name": "Tiago Bernardo", "email": "tiagorobotik@gmail.com"}, license_info={"name": "Apache 2.0","url": "https://www.apache.org/licenses/LICENSE-2.0.html",}, on_startup=[intentKit.reuse, dictionaryKit.load])

@app.get("/", name="Route")
async def roote():
    return {"name": "Alex"}


@app.get("/alex/alive", name="Check If Alive", description="This checks if alex is running and send the basic values")
async def alive():
    responce = {
        "on": True,
        "kit": {
            "all_on": True and intentKit.loaded and  dictionaryKit.loaded,
            "user": True,
            "intent": intentKit.loaded,
            "dictionary": dictionaryKit.loaded
        },
        "users": len(userKit.users), 
        "lang": {
            "trained": list(filter(lambda e: e.endswith(".yaml"),os.listdir("./features/intent_recognition/snips/data/"))), 
            "instaled": list(filter(lambda e: e.endswith(".json"),os.listdir("./features/intent_recognition/snips/dataset/"))), 
        },
        "version": __version__
        }
    return responce

@app.get("/intent_recognition/engine", name="Train or Reuse the Intent Recognition Engine")
async def intent_train(type: IntentRecongnitionEngineTrainType = IntentRecongnitionEngineTrainType.REUSE, lang: Lang = "en"):
    try:
        if type == IntentRecongnitionEngineTrainType.REUSE:
            intentKit.reuse(lang)
        else:
            intentKit.train(lang)
        return {"responce": True, "action": type.value, "lang": lang}
    except Exception:
        return {"responce": False}

@app.get("/intent_recognition/", name="Recognize intent from sentence", description="This will recognize the intent from a givin sentence and return the result parsed")
async def intent_reconize(text: Annotated[str, Query(max_length=250, min_length=2)]):
    try:
        return intentKit.parse(text)
    except AttributeError:
        return {"error": "Engine not trained"}

@app.options("/users", name="Get all users ID")
async def get_users_id() -> List[str]:
    return userKit.all()

@app.get("/users/search/name", name="Search user by name")
async def user_search_name(name: Annotated[str, Query(max_length=65, min_length=2)]):
    return {"users": userKit.search_by_name(name)}

@app.get("/users/search/tags", name="Search users by tags", description="Will search user using the tags each one has. Query is the tags name, exclude is a list of ids the exclud from the result, condition is (The sign to compare to the intensity: <, >, <=, >=, !=, =):(the Intensity of the tag) ex query=Friend, exclude=['0000000001(Master user id)'], condition = '>:50'. will return all the more that 50% friends excluding the master user.")
async def user_search(query: Annotated[str, Query(max_length=25, min_length=2)], condition: Annotated[str, Query(max_length=6, min_length=3)] = ">:0", exclude=None):
    if exclude is None:
        exclude = []
    try:
        return {"users": userKit.search_by_tags(query, condition, exclude)}
    except Exception:
        return {"error": "An error occurred"}

@app.get("/user/", name="Get user object", description="gets an user object from a given id eg: 0815636592")
async def user_get(id: Annotated[str, Query(min_length=10)]):
    return userKit.get(id)

@app.patch("/user/", name="Update user", description="Will update an user from an user object")
async def user_update(user: str):
    try:
        userKit.update_user(user)
        return {"responce":True}
    except Exception as e:
        return {"error": f"Unable to create user ({e})"}

@app.put("/user/", name="Create user", description="Will create an user from an user object")
async def user_create(user: str):
    try:
        userKit.createUser(user)
        return {"responce":True}
    except Exception as e:
        return {"error": f"Unable to create user ({e})"}

@app.delete("/user/", name="Delete user", description="Will delete an user from an given user id")
async def user_delete(id: str):
    responce = userKit.delete_user(id)
    return {"responce": responce}

@app.get("/dictionary/get", name="Get word from dictionary", description="Will return the definition of a given word. Return null if no match is found.")
async def dict_get(word: Annotated[str, Query(max_length=25, min_length=2)]):
    return dictionaryKit.get(word)

@app.get("/dictionary/get/closest", name="Get the closes match in Dictionary", description="Will get the closes match of the word found in the dictionary. and return it and others matches too. Return null if no match is found.")
async def dict_get_closest(word: Annotated[str, Query(max_length=25, min_length=2)]):
    return dictionaryKit.get_closest(word)

@app.get("/dictionary/load", name = "Load the dictionary", description="Loads the dictionary file based on the given language.")
async def load_dic(lang:Lang = Lang.EN):
    try:
        dictionaryKit.load(lang)
        return {"responce": True}
    except FileNotFoundError:
        return {"error": "Unable to load dictionary"}

@app.get("/close")
async def close():
    return {"responce": True}

@app.post("/version_control/main/upload")
async def main_upload(file: UploadFile = File(...), version = "-1.1.1", platform = PlatformType.LINUX):
    chunk = 1024 * 5
    if platform == PlatformType.LINUX:
        extension = ".zip"
    elif platform == PlatformType.MACOS:
        extension = ".app"
    else:
        extension = ".exe"

    try:
        if os.path.isfile(f"./features/version_controller/main/alex.v{version}{extension}"):
            return {"error": "Already exists"}

        with open(f"./features/version_controller/main/alex.v{version}{extension}", "wb") as f:
            while contents := file.file.read(chunk * chunk):
                f.write(contents)
    except Exception as e:
        return {"error": e}
    finally:
        file.file.close()

    return {"responce": True}

@app.post("/version_control/lib/upload")
async def lib_upload(lib_type: LibType, file: UploadFile = File(...), version = "-1.1.1", platform = PlatformType.LINUX):
    chunk = 1024 * 5

    try:
        if os.path.isfile(f"./features/version_controller/lib/{lib_type}.v{version}.zip"):
            return {"error": "Already exists"}

        with open(f"./features/version_controller/lib/{lib_type}.v{version}.zip", "wb") as f:
            while contents := file.file.read(chunk * chunk):
                f.write(contents)
    except Exception as e:
        return {"error": e}
    finally:
        file.file.close()

    return {"responce": True}

@app.get("/version_control/main/last")
def main_last(platform = PlatformType.LINUX):
    bigger = None
    name = None
    if platform == PlatformType.LINUX:
        extension = ".zip"
    elif platform == PlatformType.MACOS:
        extension = ".app"
    else:
        extension = ".exe"

    files = list(map(lambda x: x.split("/")[-1].rstrip(extension),glob.glob(f"./features/version_controller/main/*{extension}")))

    for main_core in files:
        version = main_core.split(".v")[1]
        version_core_tuple = tuple(map(lambda v: int(v), version.split(".")))
        if (bigger and version_core_tuple > bigger) or bigger is None:
            bigger = version_core_tuple
            name = main_core
    return {"name": name + extension if name is not None else None, "version": bigger, "versions": files}

@app.get("/version_control/main/get")
async def main_get(platform = PlatformType.LINUX):
    l = main_last(platform)
    if l["name"] is not None:
        return FileResponse(f"./features/version_controller/main/{l['name']}", media_type="application/octet-stream", filename=l["name"])
    else:
        return JSONResponse({"error": "Not Found"}, status_code=404)

@app.get("/version_control/lib/last")
def lib_last(lib_type: LibType):
    bigger = None
    name = None

    files = list(map(lambda x: x.split("/")[-1].rstrip(".zip"),glob.glob(f"./features/version_controller/lib/{lib_type}*.zip")))

    for lib_core in files:
        version = lib_core.split(".v")[1]
        version_core_tuple = tuple(map(lambda v: int(v), version.split(".")))
        if (bigger and version_core_tuple > bigger) or bigger is None:
            bigger = version_core_tuple
            name = lib_core
    return {"name": name + ".zip" if name is not None else None , "version": bigger, "versions": files}

@app.get("/version_control/lib/get")
async def lib_get(lib_type: LibType):
    l = lib_last(lib_type)
    if l["name"] is not None:
        return FileResponse(f"./features/version_controller/lib/{l['name']}", media_type="application/octet-stream", filename=l["name"])
    else:
        return JSONResponse({"error": "Not Found"}, status_code=404)

@app.get("/get")
async def get():
    return FileResponse("features/alex.sh")

@app.get("/lang")
async def lang_base():
    return {"responce": lingua_franca.get_supported_langs()}

@app.get("/lang/parse/extract_numbers")
def extract_numbers(text: str, short_scale: bool = True, ordinals: bool = False, lang: str = ''):
    """
            Takes in a string and extracts a list of numbers.

        Args:
            text (str): the string to extract a number from
            short_scale (bool): Use "short scale" or "long scale" for large
                numbers -- over a million.  The default is short scale, which
                is now common in most English speaking countries.
                See https://en.wikipedia.org/wiki/Names_of_large_numbers
            ordinals (bool): consider ordinal numbers, e.g. third=3 instead of 1/3
            lang (str, optional): an optional BCP-47 language code, if omitted
                                  the default language will be used.
        Returns:
            list: list of extracted numbers as floats, or empty list if none found
        """
    return {"responce": lingua_franca.parse.extract_numbers(text, short_scale, ordinals, lang)}

@app.get("/lang/parse/extract_number")
def extract_number(text, short_scale=True, ordinals=False, lang=''):
    """Takes in a string and extracts a number.

    Args:
        text (str): the string to extract a number from
        short_scale (bool): Use "short scale" or "long scale" for large
            numbers -- over a million.  The default is short scale, which
            is now common in most English speaking countries.
            See https://en.wikipedia.org/wiki/Names_of_large_numbers
        ordinals (bool): consider ordinal numbers, e.g. third=3 instead of 1/3
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        (int, float or False): The number extracted or False if the input
                               text contains no numbers
    """
    return {"responce": lingua_franca.parse.extract_number(text, short_scale, ordinals, lang)}

@app.get("/lang/parse/extract_duration")
def extract_duration(text, lang=''):
    """ Convert an english phrase into a number of seconds

    Convert things like:

    * "10 minute"
    * "2 and a half hours"
    * "3 days 8 hours 10 minutes and 49 seconds"

    into an int, representing the total number of seconds.

    The words used in the duration will be consumed, and
    the remainder returned.

    As an example, "set a timer for 5 minutes" would return
    ``(300, "set a timer for")``.

    Args:
        text (str): string containing a duration
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.

    Returns:
        (timedelta, str):
                    A tuple containing the duration and the remaining text
                    not consumed in the parsing. The first value will
                    be None if no duration is found. The text returned
                    will have whitespace stripped from the ends.
    """
    return {"responce": lingua_franca.parse.extract_duration(text, lang)}

@app.get("/lang/parse/extract_datetime")
def extract_datetime(text, lang=''):
    """
    Extracts date and time information from a sentence.  Parses many of the
    common ways that humans express dates and times, including relative dates
    like "5 days from today", "tomorrow', and "Tuesday".

    Vague terminology are given arbitrary values, like:
        - morning = 8 AM
        - afternoon = 3 PM
        - evening = 7 PM

    If a time isn't supplied or implied, the function defaults to 12 AM

    Args:
        text (str): the text to be interpreted
        lang (str): the BCP-47 code for the language to use, None uses default

    Returns:
        [:obj:`datetime`, :obj:`str`]: 'datetime' is the extracted date
            as a datetime object in the local timezone.
            'leftover_string' is the original phrase with all date and time
            related keywords stripped out. See examples for further
            clarification

            Returns 'None' if no date or time related text is found.

    Examples:

        >>> extract_datetime(
        ... "What is the weather like the day after tomorrow?",
        ... datetime(2017, 6, 30, 00, 00)
        ... )
        [datetime.datetime(2017, 7, 2, 0, 0), 'what is weather like']

        >>> extract_datetime(
        ... "Set up an appointment 2 weeks from Sunday at 5 pm",
        ... datetime(2016, 2, 19, 00, 00)
        ... )
        [datetime.datetime(2016, 3, 6, 17, 0), 'set up appointment']

        >>> extract_datetime(
        ... "Set up an appointment",
        ... datetime(2016, 2, 19, 00, 00)
        ... )
        None
    """
    return {"responce": lingua_franca.parse.extract_datetime(text, lang=lang, anchorDate=None, default_time=None)}

@app.get("/lang/parse/normalize")
def normalize(text, lang='', remove_articles=True):
    """Prepare a string for parsing

    This function prepares the given text for parsing by making
    numbers consistent, getting rid of contractions, etc.

    Args:
        text (str): the string to normalize
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        remove_articles (bool): whether to remove articles (like 'a', or
                                'the'). True by default.

    Returns:
        (str): The normalized string.
    """
    return {"responce": lingua_franca.parse.normalize(text, lang, remove_articles)}

@app.get("/lang/parse/is_fractional")
def is_fractional(input_str, short_scale=True, lang=''):
    """
    This function takes the given text and checks if it is a fraction.
    Used by most of the number exractors.

    Will return False on phrases that *contain* a fraction. Only detects
    exact matches. To pull a fraction from a string, see extract_number()

    Args:
        input_str (str): the string to check if fractional
        short_scale (bool): use short scale if True, long scale if False
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
    Returns:
        (bool) or (float): False if not a fraction, otherwise the fraction
    """
    return {"responce": lingua_franca.parse.is_fractional(input_str, short_scale, lang)}

@app.get("/lang/format/nice_number")
def nice_number(number, lang='', speech=True, denominators=[]):
    """Format a float to human readable functions

    This function formats a float to human understandable functions. Like
    4.5 becomes 4 and a half for speech and 4 1/2 for text
    Args:
        number (int or float): the float to format
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    return {"responce": lingua_franca.format.nice_number(float(number), lang, speech, list(map(lambda x: int(x), denominators)))}

@app.get("/lang/format/nice_time")
def nice_time(dt=None, lang='', speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format

    For example, generate 'five thirty' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        speech (bool): format for speech (default/True) or display (False)
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
        variant (string): alternative time system to be used, string must
                          match language specific mappings
    Returns:
        (str): The formatted time string
    """
    n = datetime.now() + timedelta(hours=1)
    return {"responce": lingua_franca.format.nice_time(dt if dt is not None else n, lang, speech, use_24hour, use_ampm)}

@app.get("/lang/format/pronounce_number")
def pronounce_number(number: int, lang='', places=2):
    """
    Convert a number to it's spoken equivalent

    For example, '5' would be 'five'

    Args:
        number: the number to pronounce
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        places (int): number of decimal places to express, default 2
    Returns:
        (str): The pronounced number
    """
    return {"responce": lingua_franca.format.pronounce_number(number, lang, places)}

@app.get("/lang/format/nice_duration")
def nice_duration(duration: int, lang='', speech=True):
    """ Convert duration in seconds to a nice spoken timespan

    Examples:
       duration = 60  ->  "1:00" or "one minute"
       duration = 163  ->  "2:43" or "two minutes forty three seconds"

    Args:
        duration: time, in seconds
        lang (str, optional): an optional BCP-47 language code, if omitted
                              the default language will be used.
        speech (bool): format for speech (True) or display (False)

    Returns:
        str: timespan as a string
    """
    return {"responce": lingua_franca.format.nice_duration(duration, lang, speech)}

@app.get("/lang/format/nice_relative_time")
def nice_relative_time(when, relative_to=None, lang=None):
    """Create a relative phrase to roughly describe the period between two
    datetimes.

    Examples are "25 seconds", "tomorrow", "7 days".

    Note: The reported period is currently limited to a number of days. Longer
          periods such as multiple weeks or months will be reported in days.

    Args:
        when (datetime): Local timezone
        relative_to (datetime): Baseline for relative time, default is now()
        lang (str, optional): Defaults to "en-us".
    Returns:
        str: Relative description of the given time
    """
    return {"responce": lingua_franca.format.nice_relative_time(when, relative_to, lang)}

def lock_pid():
    pid = os.getpid()
    with open('/home/pegasus/.alex_server', "x") as pidfile:
        pidfile.write(str(pid))

def clean():
    os.system("rm /home/pegasus/.alex_server")

def main():
    print("Started server process")
    print("Waiting for application startup.")
    print(f"App started on http://{api['HOST']}:{api['PORT']}")
    uvicorn.run(app, host=api["HOST"], port=api["PORT"], log_level="warning")

if __name__ == "__main__":
    try:
        lock_pid()
        main()
    except Exception:
        pass
    clean()