import { FORM_ERROR } from 'final-form';
import React from 'react';
import {Form as FinalForm, Field} from 'react-final-form';
import {isValidHttpUrl} from '../validators';

const FormComponent = ({handleSubmit, submitting, submitError}) => {
  return (
    <form
      style={{
        maxWidth: 500,
        width: '100%'
      }}
      className="link-form"
      onSubmit={(e) => {
        e.preventDefault();
      }}>
      <div>{submitting ? 'Please, wait...' : submitError === 'Still processing...' ? `
        The file is queued for processing.
        The app will retry to check its status every 10 seconds.
        Please wait...` : 'Paste your link here' }</div>
      <Field
        name="url"
        type="text"
        component="input"
        validate={isValidHttpUrl}>
        {({ meta, input }) => {
          return (
            <>
              <input
                {...input}
                style={{
                  width: '100%'
                }}
                onChange={(e) => {
                input.onChange(e.target.value);
                !submitting && handleSubmit();
              }} />
              <div style={{ color: 'red' }}>
                {!meta.pristine && meta.error}
              </div>
            </>
          );
        }}
      </Field>
      {submitError && <div style={{ color: 'red' }}>{submitError}</div>}
      <button
        disabled={submitting}
        onClick={handleSubmit}>
        Submit
      </button>
    </form>
  );
};

let timeout;

const Form = ({ onResult }) => {
  return (
    <div>
      <FinalForm
        component={FormComponent}
        onSubmit={async (form, formApi) => {
          const pathname = new URL(form?.url).pathname || "";

          const id = pathname.split('/status/')[1];
          if(!id) {
            return {
              [FORM_ERROR]: 'Wrong link format'
            }
          }
          const response = await fetch(process.env.REACT_APP_API_URL, {
            method: 'POST',
            body: JSON.stringify({ id }),
            headers: {
              'content-type': 'application/json'
            }
          });
          const data = await response.json();
          if(data.error) {
            if(data.error === 1000) {
              clearTimeout(timeout);
              timeout = setTimeout(() => {
                formApi.submit();
              }, 10000);
            }
            return {
              [FORM_ERROR]: data.message
            }
          } else {
            onResult(data);
          }
        }} />
    </div>
  )
};

export default Form;