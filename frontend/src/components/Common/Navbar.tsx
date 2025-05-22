import { Flex, useBreakpointValue } from "@chakra-ui/react";
import { Link as RouterLink } from "@tanstack/react-router";

import UserMenu from "./UserMenu";

function Navbar() {
  const display = useBreakpointValue({ base: "none", md: "flex" });

  return (
    <Flex
      display={display}
      justify="space-between"
      position="sticky"
      color="white"
      align="center"
      bg="bg.muted"
      w="100%"
      top={0}
      p={4}
    >
      <RouterLink
        to="/"
        className="main-link"
        style={{
          fontSize: "1.5rem",
          fontWeight: "bold",
        }}
      >
        Task Manager App
      </RouterLink>
      <Flex gap={2} alignItems="center">
        <UserMenu />
      </Flex>
    </Flex>
  );
}

export default Navbar;
