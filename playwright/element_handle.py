# Copyright (c) Microsoft Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import mimetypes
import os
import sys
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union, cast

from playwright.connection import ChannelOwner, from_nullable_channel
from playwright.helper import (
    FilePayload,
    KeyboardModifier,
    MouseButton,
    SelectOption,
    locals_to_params,
)
from playwright.js_handle import JSHandle, parse_result, serialize_argument

if sys.version_info >= (3, 8):  # pragma: no cover
    from typing import Literal
else:  # pragma: no cover
    from typing_extensions import Literal

if TYPE_CHECKING:  # pragma: no cover
    from playwright.frame import Frame


class ElementHandle(JSHandle):
    def __init__(
        self, parent: ChannelOwner, type: str, guid: str, initializer: Dict
    ) -> None:
        super().__init__(parent, type, guid, initializer)

    def asElement(self) -> Optional["ElementHandle"]:
        return self

    async def ownerFrame(self) -> Optional["Frame"]:
        return from_nullable_channel(await self._channel.send("ownerFrame"))

    async def contentFrame(self) -> Optional["Frame"]:
        return from_nullable_channel(await self._channel.send("contentFrame"))

    async def getAttribute(self, name: str) -> str:
        return await self._channel.send("getAttribute", dict(name=name))

    async def textContent(self) -> str:
        return await self._channel.send("textContent")

    async def innerText(self) -> str:
        return await self._channel.send("innerText")

    async def innerHTML(self) -> str:
        return await self._channel.send("innerHTML")

    async def dispatchEvent(self, type: str, eventInit: Dict = None) -> None:
        await self._channel.send("dispatchEvent", dict(type=type, eventInit=eventInit))

    async def scrollIntoViewIfNeeded(self, timeout: int = None) -> None:
        await self._channel.send("scrollIntoViewIfNeeded", locals_to_params(locals()))

    async def hover(
        self,
        modifiers: List[KeyboardModifier] = None,
        position: Dict = None,
        timeout: int = None,
        force: bool = None,
    ) -> None:
        await self._channel.send("hover", locals_to_params(locals()))

    async def click(
        self,
        modifiers: List[KeyboardModifier] = None,
        position: Dict = None,
        delay: int = None,
        button: MouseButton = None,
        clickCount: int = None,
        timeout: int = None,
        force: bool = None,
        noWaitAfter: bool = None,
    ) -> None:
        await self._channel.send("click", locals_to_params(locals()))

    async def dblclick(
        self,
        modifiers: List[KeyboardModifier] = None,
        position: Dict = None,
        delay: int = None,
        button: MouseButton = None,
        timeout: int = None,
        force: bool = None,
        noWaitAfter: bool = None,
    ) -> None:
        await self._channel.send("dblclick", locals_to_params(locals()))

    async def selectOption(
        self, values: "ValuesToSelect", timeout: int = None, noWaitAfter: bool = None
    ) -> List[str]:
        params = locals_to_params(locals())
        if "values" in params:
            values = params.pop("values")
            params = {**params, **convert_select_option_values(values)}
        return await self._channel.send("selectOption", params)

    async def fill(
        self, value: str, timeout: int = None, noWaitAfter: bool = None
    ) -> None:
        await self._channel.send("fill", locals_to_params(locals()))

    async def selectText(self, timeout: int = None) -> None:
        await self._channel.send("selectText", locals_to_params(locals()))

    async def setInputFiles(
        self,
        files: Union[str, FilePayload, List[str], List[FilePayload]],
        timeout: int = None,
        noWaitAfter: bool = None,
    ) -> None:
        params = locals_to_params(locals())
        params["files"] = normalize_file_payloads(files)
        await self._channel.send("setInputFiles", params)

    async def focus(self) -> None:
        await self._channel.send("focus")

    async def type(
        self,
        text: str,
        delay: int = None,
        timeout: int = None,
        noWaitAfter: bool = None,
    ) -> None:
        await self._channel.send("text", locals_to_params(locals()))

    async def press(
        self, key: str, delay: int = None, timeout: int = None, noWaitAfter: bool = None
    ) -> None:
        await self._channel.send("press", locals_to_params(locals()))

    async def check(
        self, timeout: int = None, force: bool = None, noWaitAfter: bool = None
    ) -> None:
        await self._channel.send("check", locals_to_params(locals()))

    async def uncheck(
        self, timeout: int = None, force: bool = None, noWaitAfter: bool = None
    ) -> None:
        await self._channel.send("uncheck", locals_to_params(locals()))

    async def boundingBox(self) -> Dict[str, float]:
        return await self._channel.send("boundingBox")

    async def screenshot(
        self,
        timeout: int = None,
        type: Literal["png", "jpeg"] = None,
        path: str = None,
        quality: int = None,
        omitBackground: bool = None,
    ) -> bytes:
        binary = await self._channel.send("screenshot", locals_to_params(locals()))
        return base64.b64decode(binary)

    async def querySelector(self, selector: str) -> Optional["ElementHandle"]:
        return from_nullable_channel(
            await self._channel.send("querySelector", dict(selector=selector))
        )

    async def querySelectorAll(self, selector: str) -> List["ElementHandle"]:
        return list(
            map(
                cast(Callable[[Any], Any], from_nullable_channel),
                await self._channel.send("querySelectorAll", dict(selector=selector)),
            )
        )

    async def evalOnSelector(
        self, selector: str, expression: str, arg: Any = None, force_expr: bool = False
    ) -> Any:
        return parse_result(
            await self._channel.send(
                "evalOnSelector",
                dict(
                    selector=selector,
                    expression=expression,
                    isFunction=not (force_expr),
                    arg=serialize_argument(arg),
                ),
            )
        )

    async def evalOnSelectorAll(
        self, selector: str, expression: str, arg: Any = None, force_expr: bool = False
    ) -> Any:
        return parse_result(
            await self._channel.send(
                "evalOnSelectorAll",
                dict(
                    selector=selector,
                    expression=expression,
                    isFunction=not (force_expr),
                    arg=serialize_argument(arg),
                ),
            )
        )


ValuesToSelect = Union[
    str,
    ElementHandle,
    SelectOption,
    List[str],
    List[ElementHandle],
    List[SelectOption],
    None,
]


def convert_select_option_values(arg: ValuesToSelect) -> Any:
    if arg is None:
        return {}
    arg_list = arg if isinstance(arg, list) else [arg]
    if not len(arg_list):
        return {}
    if isinstance(arg_list[0], ElementHandle):
        element_list = cast(List[ElementHandle], arg_list)
        return dict(elements=list(map(lambda e: e._channel, element_list)))
    if isinstance(arg_list[0], str):
        return dict(options=list(map(lambda e: dict(value=e), arg_list)))
    return dict(options=arg_list)


def normalize_file_payloads(
    files: Union[str, FilePayload, List[str], List[FilePayload]]
) -> List[FilePayload]:
    file_list = files if isinstance(files, list) else [files]
    file_payloads: List[FilePayload] = []
    for item in file_list:
        if isinstance(item, str):
            with open(item, mode="rb") as fd:
                file: FilePayload = {
                    "name": os.path.basename(item),
                    "mimeType": mimetypes.guess_type(item)[0]
                    or "application/octet-stream",
                    "buffer": base64.b64encode(fd.read()).decode(),
                }
                file_payloads.append(file)
        else:
            if isinstance(item["buffer"], bytes):
                item["buffer"] = base64.b64encode(item["buffer"]).decode()
            file_payloads.append(item)

    return file_payloads
