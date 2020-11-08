tensorflow.keras.layers.experimental.preprocessing里面又很多数据预处理的函数，非常好用





## TextVectorization

~~~python
class TextVectorization(CombinerPreprocessingLayer):
  """Text vectorization layer.

  This layer has basic options for managing text in a Keras model. It
  transforms a batch of strings (one sample = one string) into either a list of
  token indices (one sample = 1D tensor of integer token indices) or a dense
  representation (one sample = 1D tensor of float values representing data about
  the sample's tokens).

  If desired, the user can call this layer's adapt() method on a dataset.
  When this layer is adapted, it will analyze the dataset, determine the
  frequency of individual string values, and create a 'vocabulary' from them.
  This vocabulary can have unlimited size or be capped, depending on the
  configuration options for this layer; if there are more unique values in the
  input than the maximum vocabulary size, the most frequent terms will be used
  to create the vocabulary.

  The processing of each sample contains the following steps:

    1. standardize each sample (usually lowercasing + punctuation stripping)
    2. split each sample into substrings (usually words)
    3. recombine substrings into tokens (usually ngrams)
    4. index tokens (associate a unique int value with each token)
    5. transform each sample using this index, either into a vector of ints or
       a dense float vector.

  Some notes on passing Callables to customize splitting and normalization for
  this layer:

    1. Any callable can be passed to this Layer, but if you want to serialize
       this object you should only pass functions that are registered Keras
       serializables (see `tf.keras.utils.register_keras_serializable` for more
       details).
    2. When using a custom callable for `standardize`, the data received
       by the callable will be exactly as passed to this layer. The callable
       should return a tensor of the same shape as the input.
    3. When using a custom callable for `split`, the data received by the
       callable will have the 1st dimension squeezed out - instead of
       `[["string to split"], ["another string to split"]]`, the Callable will
       see `["string to split", "another string to split"]`. The callable should
       return a Tensor with the first dimension containing the split tokens -
       in this example, we should see something like `[["string", "to", "split],
       ["another", "string", "to", "split"]]`. This makes the callable site
       natively compatible with `tf.strings.split()`.

  Attributes:
    max_tokens: The maximum size of the vocabulary for this layer. If None,
      there is no cap on the size of the vocabulary. Note that this vocabulary
      contains 1 OOV token, so the effective number of tokens is `(max_tokens -
      1 - (1 if output == "int" else 0))`.
    standardize: Optional specification for standardization to apply to the
      input text. Values can be None (no standardization),
      'lower_and_strip_punctuation' (lowercase and remove punctuation) or a
      Callable. Default is 'lower_and_strip_punctuation'.
    split: Optional specification for splitting the input text. Values can be
      None (no splitting), 'whitespace' (split on ASCII whitespace), or a
      Callable. The default is 'whitespace'.
    ngrams: Optional specification for ngrams to create from the possibly-split
      input text. Values can be None, an integer or tuple of integers; passing
      an integer will create ngrams up to that integer, and passing a tuple of
      integers will create ngrams for the specified values in the tuple. Passing
      None means that no ngrams will be created.
    output_mode: Optional specification for the output of the layer. Values can
      be "int", "binary", "count" or "tf-idf", configuring the layer as follows:
        "int": Outputs integer indices, one integer index per split string
          token. When output == "int", 0 is reserved for masked locations;
          this reduces the vocab size to max_tokens-2 instead of max_tokens-1
        "binary": Outputs a single int array per batch, of either vocab_size or
          max_tokens size, containing 1s in all elements where the token mapped
          to that index exists at least once in the batch item.
        "count": As "binary", but the int array contains a count of the number
          of times the token at that index appeared in the batch item.
        "tf-idf": As "binary", but the TF-IDF algorithm is applied to find the
          value in each token slot.
    output_sequence_length: Only valid in INT mode. If set, the output will have
      its time dimension padded or truncated to exactly `output_sequence_length`
      values, resulting in a tensor of shape [batch_size,
      output_sequence_length] regardless of how many tokens resulted from the
      splitting step. Defaults to None.
    pad_to_max_tokens: Only valid in  "binary", "count", and "tf-idf" modes. If
      True, the output will have its feature axis padded to `max_tokens` even if
      the number of unique tokens in the vocabulary is less than max_tokens,
      resulting in a tensor of shape [batch_size, max_tokens] regardless of
      vocabulary size. Defaults to True.

  Example:
  This example instantiates a TextVectorization layer that lowercases text,
  splits on whitespace, strips punctuation, and outputs integer vocab indices.

  >>> text_dataset = tf.data.Dataset.from_tensor_slices(["foo", "bar", "baz"])
  >>> max_features = 5000  # Maximum vocab size.
  >>> max_len = 4  # Sequence length to pad the outputs to.
  >>> embedding_dims = 2
  >>>
  >>> # Create the layer.
  >>> vectorize_layer = TextVectorization(
  ...  max_tokens=max_features,
  ...  output_mode='int',
  ...  output_sequence_length=max_len)
  >>>
  >>> # Now that the vocab layer has been created, call `adapt` on the text-only
  >>> # dataset to create the vocabulary. You don't have to batch, but for large
  >>> # datasets this means we're not keeping spare copies of the dataset.
  >>> vectorize_layer.adapt(text_dataset.batch(64))
  >>>
  >>> # Create the model that uses the vectorize text layer
  >>> model = tf.keras.models.Sequential()
  >>>
  >>> # Start by creating an explicit input layer. It needs to have a shape of
  >>> # (1,) (because we need to guarantee that there is exactly one string
  >>> # input per batch), and the dtype needs to be 'string'.
  >>> model.add(tf.keras.Input(shape=(1,), dtype=tf.string))
  >>>
  >>> # The first layer in our model is the vectorization layer. After this
  >>> # layer, we have a tensor of shape (batch_size, max_len) containing vocab
  >>> # indices.
  >>> model.add(vectorize_layer)
  >>>
  >>> # Now, the model can map strings to integers, and you can add an embedding
  >>> # layer to map these integers to learned embeddings.
  >>> input_data = [["foo qux bar"], ["qux baz"]]
  >>> model.predict(input_data)
  array([[2, 1, 4, 0],
         [1, 3, 0, 0]])

  """
  # TODO(momernick): Add an examples section to the docstring.

  def __init__(self,
               max_tokens=None,
               standardize=LOWER_AND_STRIP_PUNCTUATION,
               split=SPLIT_ON_WHITESPACE,
               ngrams=None,
               output_mode=INT,
               output_sequence_length=None,
               pad_to_max_tokens=True,
               **kwargs):

    # This layer only applies to string processing, and so should only have
    # a dtype of 'string'.
    if "dtype" in kwargs and kwargs["dtype"] != dtypes.string:
      raise ValueError("TextVectorization may only have a dtype of string.")
    elif "dtype" not in kwargs:
      kwargs["dtype"] = dtypes.string

    # 'standardize' must be one of (None, LOWER_AND_STRIP_PUNCTUATION, callable)
    layer_utils.validate_string_arg(
        standardize,
        allowable_strings=(LOWER_AND_STRIP_PUNCTUATION),
        layer_name="TextVectorization",
        arg_name="standardize",
        allow_none=True,
        allow_callables=True)
~~~



1. standardize each sample (usually lowercasing + punctuation stripping)
2. split each sample into substrings (usually words)
3. recombine substrings into tokens (usually ngrams)
4. index tokens (associate a unique int value with each token)
5. transform each sample using this index, either into a vector of ints or
   a dense float vector.