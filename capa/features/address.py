# Copyright (C) 2023 Mandiant, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
# You may obtain a copy of the License at: [package root]/LICENSE.txt
# Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.
import abc


class Address(abc.ABC):
    @abc.abstractmethod
    def __eq__(self, other):
        ...

    @abc.abstractmethod
    def __lt__(self, other):
        # implement < so that addresses can be sorted from low to high
        ...

    @abc.abstractmethod
    def __hash__(self):
        # implement hash so that addresses can be used in sets and dicts
        ...

    @abc.abstractmethod
    def __repr__(self):
        # implement repr to help during debugging
        ...


class AbsoluteVirtualAddress(int, Address):
    """an absolute memory address"""

    def __new__(cls, v):
        assert v >= 0
        return int.__new__(cls, v)

    def __repr__(self):
        return f"absolute(0x{self:x})"

    def __hash__(self):
        return int.__hash__(self)


class ProcessAddress(Address):
    """an address of a process in a dynamic execution trace"""

    def __init__(self, pid: int, ppid: int = 0):
        assert ppid >= 0
        assert pid > 0
        self.ppid = ppid
        self.pid = pid

    def __repr__(self):
        return "process(%s%s)" % (
            f"ppid: {self.ppid}, " if self.ppid > 0 else "",
            f"pid: {self.pid}",
        )

    def __hash__(self):
        return hash((self.ppid, self.pid))

    def __eq__(self, other):
        assert isinstance(other, ProcessAddress)
        return (self.ppid, self.pid) == (other.ppid, other.pid)

    def __lt__(self, other):
        return (self.ppid, self.pid) < (other.ppid, other.pid)


class ThreadAddress(Address):
    """addresses a thread in a dynamic execution trace"""

    def __init__(self, process: ProcessAddress, tid: int):
        assert tid >= 0
        self.process = process
        self.tid = tid

    def __repr__(self):
        return f"thread(tid: {self.tid})"

    def __hash__(self):
        return hash((self.process, self.tid))

    def __eq__(self, other):
        assert isinstance(other, ThreadAddress)
        return (self.process, self.tid) == (other.process, other.tid)

    def __lt__(self, other):
        return (self.process, self.tid) < (other.process, other.tid)


class DynamicAddress(Address):
    """an address from a dynamic analysis trace"""

    def __init__(self, id_: int, return_address: int):
        assert id_ >= 0
        assert return_address >= 0
        self.id = id_
        self.return_address = return_address

    def __repr__(self):
        return f"dynamic(event: {self.id}, returnaddress: 0x{self.return_address:x})"

    def __hash__(self):
        return hash((self.id, self.return_address))

    def __eq__(self, other):
        return (self.id, self.return_address) == (other.id, other.return_address)

    def __lt__(self, other):
        return (self.id, self.return_address) < (other.id, other.return_address)


class RelativeVirtualAddress(int, Address):
    """a memory address relative to a base address"""

    def __repr__(self):
        return f"relative(0x{self:x})"

    def __hash__(self):
        return int.__hash__(self)


class FileOffsetAddress(int, Address):
    """an address relative to the start of a file"""

    def __new__(cls, v):
        assert v >= 0
        return int.__new__(cls, v)

    def __repr__(self):
        return f"file(0x{self:x})"

    def __hash__(self):
        return int.__hash__(self)


class DNTokenAddress(int, Address):
    """a .NET token"""

    def __new__(cls, token: int):
        return int.__new__(cls, token)

    def __repr__(self):
        return f"token(0x{self:x})"

    def __hash__(self):
        return int.__hash__(self)


class DNTokenOffsetAddress(Address):
    """an offset into an object specified by a .NET token"""

    def __init__(self, token: int, offset: int):
        assert offset >= 0
        self.token = token
        self.offset = offset

    def __eq__(self, other):
        return (self.token, self.offset) == (other.token, other.offset)

    def __lt__(self, other):
        return (self.token, self.offset) < (other.token, other.offset)

    def __hash__(self):
        return hash((self.token, self.offset))

    def __repr__(self):
        return f"token(0x{self.token:x})+(0x{self.offset:x})"

    def __index__(self):
        return self.token + self.offset


class _NoAddress(Address):
    def __eq__(self, other):
        return True

    def __lt__(self, other):
        return False

    def __hash__(self):
        return hash(0)

    def __repr__(self):
        return "no address"


NO_ADDRESS = _NoAddress()
