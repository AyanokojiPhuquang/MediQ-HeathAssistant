using System;
using System.Collections.Generic;

namespace BusinessObjects.Models;

public partial class ChatMessage
{
    public int MessageId { get; set; }

    public int SessionId { get; set; }

    public string Sender { get; set; } = null!;

    public string MessageText { get; set; } = null!;

    public DateTime? CreatedAt { get; set; }

    public virtual ChatSession Session { get; set; } = null!;
}
