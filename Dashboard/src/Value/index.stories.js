import React from 'react'
import { action } from '@storybook/addon-actions'
import Quote from './index'

const quote = "Perhaps I should have been more like water today"

export default {
  title: 'Quote',
  component: Quote,
}

export const Default = () => (
  <Quote quote={quote} quoter={"Kanye"}/>
)
