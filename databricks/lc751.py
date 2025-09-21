from typing import List

"""
An IP address is a formatted 32-bit unsigned integer where each group of 8 bits is printed as a decimal number and the dot character '.' splits the groups.

For example, the binary number 00001111 10001000 11111111 01101011 (spaces added for clarity) formatted as an IP address would be "15.136.255.107".
A CIDR block is a format used to denote a specific set of IP addresses. It is a string consisting of a base IP address, followed by a slash, followed by a prefix length k. The addresses it covers are all the IPs whose first k bits are the same as the base IP address.

For example, "123.45.67.89/20" is a CIDR block with a prefix length of 20. Any IP address whose binary representation matches 01111011 00101101 0100xxxx xxxxxxxx, where x can be either 0 or 1, is in the set covered by the CIDR block.
You are given a start IP address ip and the number of IP addresses we need to cover n. Your goal is to use as few CIDR blocks as possible to cover all the IP addresses in the inclusive range [ip, ip + n - 1] exactly. No other IP addresses outside of the range should be covered.

Return the shortest list of CIDR blocks that covers the range of IP addresses. If there are multiple answers, return any of them.
"""


class Solution:
    """
    input: start address, num of IP addresses we need to cover -> [ip, ip + n - 1]
    return: shortest list of CIDR blocks the covers the minimum set of IP addresses []

    how many bits are in common?
    you have "255.0.0.7 and you need to get to 255.0.0.16"
    start from the start -> how many IP addresses can you represent with this?
    decrease the prefix length and try the next bit check to not go over (set that represents too
        many addresses

    Convert the ip addresses to and from (long) integers. You want to know what is the most addresses you can put in this block starting from the "start" ip, up to n. It is the smallest between the lowest bit of start and the highest bit of n. Then, repeat this process with a new start and n.

    """

    # convert starting ip address to int
    def ipToInt(self, ip: str) -> int:
        # split ip, shift x bits left, add to result
        ip = ip.split(".")
        BITS_PER_BLOCK = 8
        res = 0
        for i in range(3):
            adder = int(ip[i]) << (abs(i - 3) * BITS_PER_BLOCK)
            res += adder

        return res + int(ip[3])

    # convert from int to ip address
    def IntToIp(self, val: int) -> str:
        # shift right and mask to get the rightmost x bits
        # convert to string, add to list, then append
        BIT_MASK = 255
        BITS_PER_BLOCK = 8
        res = []
        for i in range(3, -1, -1):
            octet = (val >> (i * BITS_PER_BLOCK)) & BIT_MASK
            res.append(str(octet))

        return ".".join(res)

    def ipToCIDR(self, ip: str, n: int) -> List[str]:
        """
        You'll need a loop that continues as long as n (the number of IPs to cover) is greater than zero. Inside the loop, you'll perform these steps:
        Calculate the Block Size: This is the most important step. You need to find the size of the block you're going to create. As we discussed, this size is the minimum of two values:
        The largest block the starting IP allows. A great trick for this is the bitwise operation start_ip & -start_ip. This isolates the lowest set bit, which is exactly the largest power of 2 that divides start_ip.
        The largest block the remaining n allows. This is the largest power of 2 that is less than or equal to n.
        Calculate the Prefix Length: Once you have the block size (which will be a power of 2, like 8), you need to convert it to a prefix length. You can do this by finding the exponent. For example, since 8=2
        3
         , the number of bits for the host is 3. The prefix length is then 32−3=29. The result is a /29.
        Construct and Store the CIDR String: Use your IntToIp helper to convert the current start_ip back to a string, then append the slash and the prefix length you just calculated. Add this string to your results list.
        Update for the Next Iteration:
        Add the block size to start_ip.
        Subtract the block size from n.
        Repeat this process until n is zero, and you will have your complete list of CIDR blocks.
        """
        startip = self.ipToInt(ip)
        result = []
        while n > 0:
            # find the rightmost bit position -> # of blocks that can be represented
            if startip == 0:
                block_size = n  # can start anywhere when IP is 0
            else:
                block_size = startip & -startip

            largest_possible_block = 1 << (n.bit_length() - 1)

            max_block_length = min(block_size, largest_possible_block)
            num_bits = max_block_length.bit_length() - 1
            prefix_length = 32 - num_bits
            temp = self.IntToIp(startip) + "/" + str(prefix_length)
            result.append(temp)

            startip += max_block_length
            n -= max_block_length

        return result


def main():
    obj = Solution()

    assert obj.ipToCIDR("255.0.0.7", 10) == [
        "255.0.0.7/32",
        "255.0.0.8/29",
        "255.0.0.16/32",
    ]
    assert obj.ipToCIDR("117.145.102.62", 8) == [
        "117.145.102.62/31",
        "117.145.102.64/30",
        "117.145.102.68/31",
    ]


if __name__ == "__main__":
    main()
