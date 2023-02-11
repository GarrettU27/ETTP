import {MainButton} from "../components/Button";
import styled from "styled-components";
import {useNavigate, useNavigation} from "react-router-dom";
import React from "react";
import loadingIcon from "../loading-icon.gif"

const Center = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2em;
  width: 50%;
  margin: 8em auto;
  justify-content: center;
`

const LoadingImage = styled.img`
  width: 5%;
`

const LoadingDiv = styled.div`
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`

function Root() {
  const navigation = useNavigation()
  const navigate = useNavigate();

  return(
    <Center>
      <MainButton onClick={() => navigate("/training")}>Training</MainButton>
      <MainButton onClick={() => navigate("/testing")}>Test</MainButton>
      {
        navigation.state === "loading" ?
          <LoadingDiv>
            <LoadingImage src={loadingIcon}  alt={"Loading Icon"}/>
          </LoadingDiv>
          :
          null
      }
    </Center>
  )
}

export default Root;
